r'''
# `google_compute_backend_service`

Refer to the Terraform Registry for docs: [`google_compute_backend_service`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service).
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


class GoogleComputeBackendService(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendService",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service google_compute_backend_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        affinity_cookie_ttl_sec: typing.Optional[jsii.Number] = None,
        backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceBackend", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cdn_policy: typing.Optional[typing.Union["GoogleComputeBackendServiceCdnPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        circuit_breakers: typing.Optional[typing.Union["GoogleComputeBackendServiceCircuitBreakers", typing.Dict[builtins.str, typing.Any]]] = None,
        compression_mode: typing.Optional[builtins.str] = None,
        connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
        consistent_hash: typing.Optional[typing.Union["GoogleComputeBackendServiceConsistentHash", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceCustomMetrics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_request_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_response_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamic_forwarding: typing.Optional[typing.Union["GoogleComputeBackendServiceDynamicForwarding", typing.Dict[builtins.str, typing.Any]]] = None,
        edge_security_policy: typing.Optional[builtins.str] = None,
        enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_managed_migration_state: typing.Optional[builtins.str] = None,
        external_managed_migration_testing_percentage: typing.Optional[jsii.Number] = None,
        health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        iap: typing.Optional[typing.Union["GoogleComputeBackendServiceIap", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address_selection_policy: typing.Optional[builtins.str] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        locality_lb_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceLocalityLbPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        locality_lb_policy: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["GoogleComputeBackendServiceLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        max_stream_duration: typing.Optional[typing.Union["GoogleComputeBackendServiceMaxStreamDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        network_pass_through_lb_traffic_policy: typing.Optional[typing.Union["GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        outlier_detection: typing.Optional[typing.Union["GoogleComputeBackendServiceOutlierDetection", typing.Dict[builtins.str, typing.Any]]] = None,
        port_name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        security_policy: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[typing.Union["GoogleComputeBackendServiceSecuritySettings", typing.Dict[builtins.str, typing.Any]]] = None,
        service_lb_policy: typing.Optional[builtins.str] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        strong_session_affinity_cookie: typing.Optional[typing.Union["GoogleComputeBackendServiceStrongSessionAffinityCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeBackendServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_sec: typing.Optional[jsii.Number] = None,
        tls_settings: typing.Optional[typing.Union["GoogleComputeBackendServiceTlsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service google_compute_backend_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        :param affinity_cookie_ttl_sec: Lifetime of cookies in seconds if session_affinity is GENERATED_COOKIE. If set to 0, the cookie is non-persistent and lasts only until the end of the browser session (or equivalent). The maximum allowed value for TTL is one day. When the load balancing scheme is INTERNAL, this field is not used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#affinity_cookie_ttl_sec GoogleComputeBackendService#affinity_cookie_ttl_sec}
        :param backend: backend block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#backend GoogleComputeBackendService#backend}
        :param cdn_policy: cdn_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#cdn_policy GoogleComputeBackendService#cdn_policy}
        :param circuit_breakers: circuit_breakers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#circuit_breakers GoogleComputeBackendService#circuit_breakers}
        :param compression_mode: Compress text responses using Brotli or gzip compression, based on the client's Accept-Encoding header. Possible values: ["AUTOMATIC", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#compression_mode GoogleComputeBackendService#compression_mode}
        :param connection_draining_timeout_sec: Time for which instance will be drained (not accept new connections, but still work to finish started). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#connection_draining_timeout_sec GoogleComputeBackendService#connection_draining_timeout_sec}
        :param consistent_hash: consistent_hash block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#consistent_hash GoogleComputeBackendService#consistent_hash}
        :param custom_metrics: custom_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#custom_metrics GoogleComputeBackendService#custom_metrics}
        :param custom_request_headers: Headers that the HTTP/S load balancer should add to proxied requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#custom_request_headers GoogleComputeBackendService#custom_request_headers}
        :param custom_response_headers: Headers that the HTTP/S load balancer should add to proxied responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#custom_response_headers GoogleComputeBackendService#custom_response_headers}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#description GoogleComputeBackendService#description}
        :param dynamic_forwarding: dynamic_forwarding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#dynamic_forwarding GoogleComputeBackendService#dynamic_forwarding}
        :param edge_security_policy: The resource URL for the edge security policy associated with this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#edge_security_policy GoogleComputeBackendService#edge_security_policy}
        :param enable_cdn: If true, enable Cloud CDN for this BackendService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enable_cdn GoogleComputeBackendService#enable_cdn}
        :param external_managed_migration_state: Specifies the canary migration state. Possible values are PREPARE, TEST_BY_PERCENTAGE, and TEST_ALL_TRAFFIC. To begin the migration from EXTERNAL to EXTERNAL_MANAGED, the state must be changed to PREPARE. The state must be changed to TEST_ALL_TRAFFIC before the loadBalancingScheme can be changed to EXTERNAL_MANAGED. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate traffic by percentage using externalManagedMigrationTestingPercentage. Rolling back a migration requires the states to be set in reverse order. So changing the scheme from EXTERNAL_MANAGED to EXTERNAL requires the state to be set to TEST_ALL_TRAFFIC at the same time. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate some traffic back to EXTERNAL or PREPARE can be used to migrate all traffic back to EXTERNAL. Possible values: ["PREPARE", "TEST_BY_PERCENTAGE", "TEST_ALL_TRAFFIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#external_managed_migration_state GoogleComputeBackendService#external_managed_migration_state}
        :param external_managed_migration_testing_percentage: Determines the fraction of requests that should be processed by the Global external Application Load Balancer. The value of this field must be in the range [0, 100]. Session affinity options will slightly affect this routing behavior, for more details, see: Session Affinity. This value can only be set if the loadBalancingScheme in the backend service is set to EXTERNAL (when using the Classic ALB) and the migration state is TEST_BY_PERCENTAGE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#external_managed_migration_testing_percentage GoogleComputeBackendService#external_managed_migration_testing_percentage}
        :param health_checks: The set of URLs to the HttpHealthCheck or HttpsHealthCheck resource for health checking this BackendService. Currently at most one health check can be specified. A health check must be specified unless the backend service uses an internet or serverless NEG as a backend. For internal load balancing, a URL to a HealthCheck resource must be specified instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#health_checks GoogleComputeBackendService#health_checks}
        :param iap: iap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#iap GoogleComputeBackendService#iap}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#id GoogleComputeBackendService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address_selection_policy: Specifies preference of traffic to the backend (from the proxy and from the client for proxyless gRPC). Possible values: ["IPV4_ONLY", "PREFER_IPV6", "IPV6_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#ip_address_selection_policy GoogleComputeBackendService#ip_address_selection_policy}
        :param load_balancing_scheme: Indicates whether the backend service will be used with internal or external load balancing. A backend service created for one type of load balancing cannot be used with the other. For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "INTERNAL_SELF_MANAGED", "INTERNAL_MANAGED", "EXTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#load_balancing_scheme GoogleComputeBackendService#load_balancing_scheme}
        :param locality_lb_policies: locality_lb_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#locality_lb_policies GoogleComputeBackendService#locality_lb_policies}
        :param locality_lb_policy: The load balancing algorithm used within the scope of the locality. The possible values are:. - 'ROUND_ROBIN': This is a simple policy in which each healthy backend is selected in round robin order. - 'LEAST_REQUEST': An O(1) algorithm which selects two random healthy hosts and picks the host which has fewer active requests. - 'RING_HASH': The ring/modulo hash load balancer implements consistent hashing to backends. The algorithm has the property that the addition/removal of a host from a set of N hosts only affects 1/N of the requests. - 'RANDOM': The load balancer selects a random healthy host. - 'ORIGINAL_DESTINATION': Backend host is selected based on the client connection metadata, i.e., connections are opened to the same address as the destination address of the incoming connection before the connection was redirected to the load balancer. - 'MAGLEV': used as a drop in replacement for the ring hash load balancer. Maglev is not as stable as ring hash but has faster table lookup build times and host selection times. For more information about Maglev, refer to https://ai.google/research/pubs/pub44824 - 'WEIGHTED_MAGLEV': Per-instance weighted Load Balancing via health check reported weights. Only applicable to loadBalancingScheme EXTERNAL. If set, the Backend Service must configure a non legacy HTTP-based Health Check, and health check replies are expected to contain non-standard HTTP response header field X-Load-Balancing-Endpoint-Weight to specify the per-instance weights. If set, Load Balancing is weight based on the per-instance weights reported in the last processed health check replies, as long as every instance either reported a valid weight or had UNAVAILABLE_WEIGHT. Otherwise, Load Balancing remains equal-weight. - 'WEIGHTED_ROUND_ROBIN': Per-endpoint weighted round-robin Load Balancing using weights computed from Backend reported Custom Metrics. If set, the Backend Service responses are expected to contain non-standard HTTP response header field X-Endpoint-Load-Metrics. The reported metrics to use for computing the weights are specified via the backends[].customMetrics fields. locality_lb_policy is applicable to either: - A regional backend service with the service_protocol set to HTTP, HTTPS, HTTP2 or H2C, and loadBalancingScheme set to INTERNAL_MANAGED. - A global backend service with the load_balancing_scheme set to INTERNAL_SELF_MANAGED. - A regional backend service with loadBalancingScheme set to EXTERNAL (External Network Load Balancing). Only MAGLEV and WEIGHTED_MAGLEV values are possible for External Network Load Balancing. The default is MAGLEV. If session_affinity is not NONE, and locality_lb_policy is not set to MAGLEV, WEIGHTED_MAGLEV, or RING_HASH, session affinity settings will not take effect. Only ROUND_ROBIN and RING_HASH are supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validate_for_proxyless field set to true. Possible values: ["ROUND_ROBIN", "LEAST_REQUEST", "RING_HASH", "RANDOM", "ORIGINAL_DESTINATION", "MAGLEV", "WEIGHTED_MAGLEV", "WEIGHTED_ROUND_ROBIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#locality_lb_policy GoogleComputeBackendService#locality_lb_policy}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#log_config GoogleComputeBackendService#log_config}
        :param max_stream_duration: max_stream_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_stream_duration GoogleComputeBackendService#max_stream_duration}
        :param network_pass_through_lb_traffic_policy: network_pass_through_lb_traffic_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#network_pass_through_lb_traffic_policy GoogleComputeBackendService#network_pass_through_lb_traffic_policy}
        :param outlier_detection: outlier_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#outlier_detection GoogleComputeBackendService#outlier_detection}
        :param port_name: Name of backend port. The same name should appear in the instance groups referenced by this service. Required when the load balancing scheme is EXTERNAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#port_name GoogleComputeBackendService#port_name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#project GoogleComputeBackendService#project}.
        :param protocol: The protocol this BackendService uses to communicate with backends. The default is HTTP. Possible values are HTTP, HTTPS, HTTP2, H2C, TCP, SSL, UDP or GRPC. Refer to the documentation for the load balancers or for Traffic Director for more information. Must be set to GRPC when the backend service is referenced by a URL map that is bound to target gRPC proxy. Possible values: ["HTTP", "HTTPS", "HTTP2", "TCP", "SSL", "UDP", "GRPC", "UNSPECIFIED", "H2C"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#protocol GoogleComputeBackendService#protocol}
        :param security_policy: The security policy associated with this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#security_policy GoogleComputeBackendService#security_policy}
        :param security_settings: security_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#security_settings GoogleComputeBackendService#security_settings}
        :param service_lb_policy: URL to networkservices.ServiceLbPolicy resource. Can only be set if load balancing scheme is EXTERNAL, EXTERNAL_MANAGED, INTERNAL_MANAGED or INTERNAL_SELF_MANAGED and the scope is global. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#service_lb_policy GoogleComputeBackendService#service_lb_policy}
        :param session_affinity: Type of session affinity to use. The default is NONE. Session affinity is not applicable if the protocol is UDP. Possible values: ["NONE", "CLIENT_IP", "CLIENT_IP_PORT_PROTO", "CLIENT_IP_PROTO", "GENERATED_COOKIE", "HEADER_FIELD", "HTTP_COOKIE", "STRONG_COOKIE_AFFINITY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#session_affinity GoogleComputeBackendService#session_affinity}
        :param strong_session_affinity_cookie: strong_session_affinity_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#strong_session_affinity_cookie GoogleComputeBackendService#strong_session_affinity_cookie}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#timeouts GoogleComputeBackendService#timeouts}
        :param timeout_sec: The backend service timeout has a different meaning depending on the type of load balancer. For more information see, `Backend service settings <https://cloud.google.com/compute/docs/reference/rest/v1/backendServices>`_. The default is 30 seconds. The full range of timeout values allowed goes from 1 through 2,147,483,647 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#timeout_sec GoogleComputeBackendService#timeout_sec}
        :param tls_settings: tls_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#tls_settings GoogleComputeBackendService#tls_settings}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c76ef557448049507f2373ae42c7c6fba4f5b6a05fb1e2ecbdb3d2661f976e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeBackendServiceConfig(
            name=name,
            affinity_cookie_ttl_sec=affinity_cookie_ttl_sec,
            backend=backend,
            cdn_policy=cdn_policy,
            circuit_breakers=circuit_breakers,
            compression_mode=compression_mode,
            connection_draining_timeout_sec=connection_draining_timeout_sec,
            consistent_hash=consistent_hash,
            custom_metrics=custom_metrics,
            custom_request_headers=custom_request_headers,
            custom_response_headers=custom_response_headers,
            description=description,
            dynamic_forwarding=dynamic_forwarding,
            edge_security_policy=edge_security_policy,
            enable_cdn=enable_cdn,
            external_managed_migration_state=external_managed_migration_state,
            external_managed_migration_testing_percentage=external_managed_migration_testing_percentage,
            health_checks=health_checks,
            iap=iap,
            id=id,
            ip_address_selection_policy=ip_address_selection_policy,
            load_balancing_scheme=load_balancing_scheme,
            locality_lb_policies=locality_lb_policies,
            locality_lb_policy=locality_lb_policy,
            log_config=log_config,
            max_stream_duration=max_stream_duration,
            network_pass_through_lb_traffic_policy=network_pass_through_lb_traffic_policy,
            outlier_detection=outlier_detection,
            port_name=port_name,
            project=project,
            protocol=protocol,
            security_policy=security_policy,
            security_settings=security_settings,
            service_lb_policy=service_lb_policy,
            session_affinity=session_affinity,
            strong_session_affinity_cookie=strong_session_affinity_cookie,
            timeouts=timeouts,
            timeout_sec=timeout_sec,
            tls_settings=tls_settings,
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
        '''Generates CDKTF code for importing a GoogleComputeBackendService resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeBackendService to import.
        :param import_from_id: The id of the existing GoogleComputeBackendService that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeBackendService to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__313b202239fa6b7a87099322cf9a8af6529f00b1b80682bb4072d1c2489ca9f0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackend")
    def put_backend(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceBackend", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f0b0a2be96eef43fdff3354257f1dc0184bd35d0b725da2e7b35336b14cd31f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackend", [value]))

    @jsii.member(jsii_name="putCdnPolicy")
    def put_cdn_policy(
        self,
        *,
        bypass_cache_on_request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cache_key_policy: typing.Optional[typing.Union["GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_mode: typing.Optional[builtins.str] = None,
        client_ttl: typing.Optional[jsii.Number] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        max_ttl: typing.Optional[jsii.Number] = None,
        negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negative_caching_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_coalescing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        serve_while_stale: typing.Optional[jsii.Number] = None,
        signed_url_cache_max_age_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bypass_cache_on_request_headers: bypass_cache_on_request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#bypass_cache_on_request_headers GoogleComputeBackendService#bypass_cache_on_request_headers}
        :param cache_key_policy: cache_key_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#cache_key_policy GoogleComputeBackendService#cache_key_policy}
        :param cache_mode: Specifies the cache setting for all responses from this backend. The possible values are: USE_ORIGIN_HEADERS, FORCE_CACHE_ALL and CACHE_ALL_STATIC Possible values: ["USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "CACHE_ALL_STATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#cache_mode GoogleComputeBackendService#cache_mode}
        :param client_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#client_ttl GoogleComputeBackendService#client_ttl}
        :param default_ttl: Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#default_ttl GoogleComputeBackendService#default_ttl}
        :param max_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_ttl GoogleComputeBackendService#max_ttl}
        :param negative_caching: Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#negative_caching GoogleComputeBackendService#negative_caching}
        :param negative_caching_policy: negative_caching_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#negative_caching_policy GoogleComputeBackendService#negative_caching_policy}
        :param request_coalescing: If true then Cloud CDN will combine multiple concurrent cache fill requests into a small number of requests to the origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#request_coalescing GoogleComputeBackendService#request_coalescing}
        :param serve_while_stale: Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#serve_while_stale GoogleComputeBackendService#serve_while_stale}
        :param signed_url_cache_max_age_sec: Maximum number of seconds the response to a signed URL request will be considered fresh, defaults to 1hr (3600s). After this time period, the response will be revalidated before being served. When serving responses to signed URL requests, Cloud CDN will internally behave as though all responses from this backend had a "Cache-Control: public, max-age=[TTL]" header, regardless of any existing Cache-Control header. The actual headers served in responses will not be altered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#signed_url_cache_max_age_sec GoogleComputeBackendService#signed_url_cache_max_age_sec}
        '''
        value = GoogleComputeBackendServiceCdnPolicy(
            bypass_cache_on_request_headers=bypass_cache_on_request_headers,
            cache_key_policy=cache_key_policy,
            cache_mode=cache_mode,
            client_ttl=client_ttl,
            default_ttl=default_ttl,
            max_ttl=max_ttl,
            negative_caching=negative_caching,
            negative_caching_policy=negative_caching_policy,
            request_coalescing=request_coalescing,
            serve_while_stale=serve_while_stale,
            signed_url_cache_max_age_sec=signed_url_cache_max_age_sec,
        )

        return typing.cast(None, jsii.invoke(self, "putCdnPolicy", [value]))

    @jsii.member(jsii_name="putCircuitBreakers")
    def put_circuit_breakers(
        self,
        *,
        connect_timeout: typing.Optional[typing.Union["GoogleComputeBackendServiceCircuitBreakersConnectTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
        max_connections: typing.Optional[jsii.Number] = None,
        max_pending_requests: typing.Optional[jsii.Number] = None,
        max_requests: typing.Optional[jsii.Number] = None,
        max_requests_per_connection: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connect_timeout: connect_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#connect_timeout GoogleComputeBackendService#connect_timeout}
        :param max_connections: The maximum number of connections to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_connections GoogleComputeBackendService#max_connections}
        :param max_pending_requests: The maximum number of pending requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_pending_requests GoogleComputeBackendService#max_pending_requests}
        :param max_requests: The maximum number of parallel requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_requests GoogleComputeBackendService#max_requests}
        :param max_requests_per_connection: Maximum requests for a single backend connection. This parameter is respected by both the HTTP/1.1 and HTTP/2 implementations. If not specified, there is no limit. Setting this parameter to 1 will effectively disable keep alive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_requests_per_connection GoogleComputeBackendService#max_requests_per_connection}
        :param max_retries: The maximum number of parallel retries to the backend cluster. Defaults to 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_retries GoogleComputeBackendService#max_retries}
        '''
        value = GoogleComputeBackendServiceCircuitBreakers(
            connect_timeout=connect_timeout,
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
        http_cookie: typing.Optional[typing.Union["GoogleComputeBackendServiceConsistentHashHttpCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        http_header_name: typing.Optional[builtins.str] = None,
        minimum_ring_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_cookie: http_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#http_cookie GoogleComputeBackendService#http_cookie}
        :param http_header_name: The hash based on the value of the specified header field. This field is applicable if the sessionAffinity is set to HEADER_FIELD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#http_header_name GoogleComputeBackendService#http_header_name}
        :param minimum_ring_size: The minimum number of virtual nodes to use for the hash ring. Larger ring sizes result in more granular load distributions. If the number of hosts in the load balancing pool is larger than the ring size, each host will be assigned a single virtual node. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#minimum_ring_size GoogleComputeBackendService#minimum_ring_size}
        '''
        value = GoogleComputeBackendServiceConsistentHash(
            http_cookie=http_cookie,
            http_header_name=http_header_name,
            minimum_ring_size=minimum_ring_size,
        )

        return typing.cast(None, jsii.invoke(self, "putConsistentHash", [value]))

    @jsii.member(jsii_name="putCustomMetrics")
    def put_custom_metrics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceCustomMetrics", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b5d6b372ea71e815a3055f7b7e1cb687eb607dc36db726ddbc73a236472cca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomMetrics", [value]))

    @jsii.member(jsii_name="putDynamicForwarding")
    def put_dynamic_forwarding(
        self,
        *,
        ip_port_selection: typing.Optional[typing.Union["GoogleComputeBackendServiceDynamicForwardingIpPortSelection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ip_port_selection: ip_port_selection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#ip_port_selection GoogleComputeBackendService#ip_port_selection}
        '''
        value = GoogleComputeBackendServiceDynamicForwarding(
            ip_port_selection=ip_port_selection
        )

        return typing.cast(None, jsii.invoke(self, "putDynamicForwarding", [value]))

    @jsii.member(jsii_name="putIap")
    def put_iap(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        oauth2_client_id: typing.Optional[builtins.str] = None,
        oauth2_client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Whether the serving infrastructure will authenticate and authorize all incoming requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enabled GoogleComputeBackendService#enabled}
        :param oauth2_client_id: OAuth2 Client ID for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#oauth2_client_id GoogleComputeBackendService#oauth2_client_id}
        :param oauth2_client_secret: OAuth2 Client Secret for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#oauth2_client_secret GoogleComputeBackendService#oauth2_client_secret}
        '''
        value = GoogleComputeBackendServiceIap(
            enabled=enabled,
            oauth2_client_id=oauth2_client_id,
            oauth2_client_secret=oauth2_client_secret,
        )

        return typing.cast(None, jsii.invoke(self, "putIap", [value]))

    @jsii.member(jsii_name="putLocalityLbPolicies")
    def put_locality_lb_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceLocalityLbPolicies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d76dee49ea4344eb0e8b2ea3b2d1b342593b4a9381f5cd96cbf16919c8601d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLocalityLbPolicies", [value]))

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
        :param enable: Whether to enable logging for the load balancer traffic served by this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enable GoogleComputeBackendService#enable}
        :param optional_fields: This field can only be specified if logging is enabled for this backend service and "logConfig.optionalMode" was set to CUSTOM. Contains a list of optional fields you want to include in the logs. For example: serverInstance, serverGkeDetails.cluster, serverGkeDetails.pod.podNamespace For example: orca_load_report, tls.protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#optional_fields GoogleComputeBackendService#optional_fields}
        :param optional_mode: Specifies the optional logging mode for the load balancer traffic. Supported values: INCLUDE_ALL_OPTIONAL, EXCLUDE_ALL_OPTIONAL, CUSTOM. Possible values: ["INCLUDE_ALL_OPTIONAL", "EXCLUDE_ALL_OPTIONAL", "CUSTOM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#optional_mode GoogleComputeBackendService#optional_mode}
        :param sample_rate: This field can only be specified if logging is enabled for this backend service. The value of the field must be in [0, 1]. This configures the sampling rate of requests to the load balancer where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported. The default value is 1.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#sample_rate GoogleComputeBackendService#sample_rate}
        '''
        value = GoogleComputeBackendServiceLogConfig(
            enable=enable,
            optional_fields=optional_fields,
            optional_mode=optional_mode,
            sample_rate=sample_rate,
        )

        return typing.cast(None, jsii.invoke(self, "putLogConfig", [value]))

    @jsii.member(jsii_name="putMaxStreamDuration")
    def put_max_stream_duration(
        self,
        *,
        seconds: builtins.str,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. (int64 format). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        value = GoogleComputeBackendServiceMaxStreamDuration(
            seconds=seconds, nanos=nanos
        )

        return typing.cast(None, jsii.invoke(self, "putMaxStreamDuration", [value]))

    @jsii.member(jsii_name="putNetworkPassThroughLbTrafficPolicy")
    def put_network_pass_through_lb_traffic_policy(
        self,
        *,
        zonal_affinity: typing.Optional[typing.Union["GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param zonal_affinity: zonal_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#zonal_affinity GoogleComputeBackendService#zonal_affinity}
        '''
        value = GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy(
            zonal_affinity=zonal_affinity
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkPassThroughLbTrafficPolicy", [value]))

    @jsii.member(jsii_name="putOutlierDetection")
    def put_outlier_detection(
        self,
        *,
        base_ejection_time: typing.Optional[typing.Union["GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime", typing.Dict[builtins.str, typing.Any]]] = None,
        consecutive_errors: typing.Optional[jsii.Number] = None,
        consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_errors: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_success_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[typing.Union["GoogleComputeBackendServiceOutlierDetectionInterval", typing.Dict[builtins.str, typing.Any]]] = None,
        max_ejection_percent: typing.Optional[jsii.Number] = None,
        success_rate_minimum_hosts: typing.Optional[jsii.Number] = None,
        success_rate_request_volume: typing.Optional[jsii.Number] = None,
        success_rate_stdev_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param base_ejection_time: base_ejection_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#base_ejection_time GoogleComputeBackendService#base_ejection_time}
        :param consecutive_errors: Number of errors before a host is ejected from the connection pool. When the backend host is accessed over HTTP, a 5xx return code qualifies as an error. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#consecutive_errors GoogleComputeBackendService#consecutive_errors}
        :param consecutive_gateway_failure: The number of consecutive gateway failures (502, 503, 504 status or connection errors that are mapped to one of those status codes) before a consecutive gateway failure ejection occurs. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#consecutive_gateway_failure GoogleComputeBackendService#consecutive_gateway_failure}
        :param enforcing_consecutive_errors: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive 5xx. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enforcing_consecutive_errors GoogleComputeBackendService#enforcing_consecutive_errors}
        :param enforcing_consecutive_gateway_failure: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive gateway failures. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enforcing_consecutive_gateway_failure GoogleComputeBackendService#enforcing_consecutive_gateway_failure}
        :param enforcing_success_rate: The percentage chance that a host will be actually ejected when an outlier status is detected through success rate statistics. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enforcing_success_rate GoogleComputeBackendService#enforcing_success_rate}
        :param interval: interval block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#interval GoogleComputeBackendService#interval}
        :param max_ejection_percent: Maximum percentage of hosts in the load balancing pool for the backend service that can be ejected. Defaults to 10%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_ejection_percent GoogleComputeBackendService#max_ejection_percent}
        :param success_rate_minimum_hosts: The number of hosts in a cluster that must have enough request volume to detect success rate outliers. If the number of hosts is less than this setting, outlier detection via success rate statistics is not performed for any host in the cluster. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#success_rate_minimum_hosts GoogleComputeBackendService#success_rate_minimum_hosts}
        :param success_rate_request_volume: The minimum number of total requests that must be collected in one interval (as defined by the interval duration above) to include this host in success rate based outlier detection. If the volume is lower than this setting, outlier detection via success rate statistics is not performed for that host. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#success_rate_request_volume GoogleComputeBackendService#success_rate_request_volume}
        :param success_rate_stdev_factor: This factor is used to determine the ejection threshold for success rate outlier ejection. The ejection threshold is the difference between the mean success rate, and the product of this factor and the standard deviation of the mean success rate: mean - (stdev * success_rate_stdev_factor). This factor is divided by a thousand to get a double. That is, if the desired factor is 1.9, the runtime value should be 1900. Defaults to 1900. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#success_rate_stdev_factor GoogleComputeBackendService#success_rate_stdev_factor}
        '''
        value = GoogleComputeBackendServiceOutlierDetection(
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

    @jsii.member(jsii_name="putSecuritySettings")
    def put_security_settings(
        self,
        *,
        aws_v4_authentication: typing.Optional[typing.Union["GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication", typing.Dict[builtins.str, typing.Any]]] = None,
        client_tls_policy: typing.Optional[builtins.str] = None,
        subject_alt_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param aws_v4_authentication: aws_v4_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#aws_v4_authentication GoogleComputeBackendService#aws_v4_authentication}
        :param client_tls_policy: ClientTlsPolicy is a resource that specifies how a client should authenticate connections to backends of a service. This resource itself does not affect configuration unless it is attached to a backend service resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#client_tls_policy GoogleComputeBackendService#client_tls_policy}
        :param subject_alt_names: A list of alternate names to verify the subject identity in the certificate. If specified, the client will verify that the server certificate's subject alt name matches one of the specified values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#subject_alt_names GoogleComputeBackendService#subject_alt_names}
        '''
        value = GoogleComputeBackendServiceSecuritySettings(
            aws_v4_authentication=aws_v4_authentication,
            client_tls_policy=client_tls_policy,
            subject_alt_names=subject_alt_names,
        )

        return typing.cast(None, jsii.invoke(self, "putSecuritySettings", [value]))

    @jsii.member(jsii_name="putStrongSessionAffinityCookie")
    def put_strong_session_affinity_cookie(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[typing.Union["GoogleComputeBackendServiceStrongSessionAffinityCookieTtl", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#path GoogleComputeBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#ttl GoogleComputeBackendService#ttl}
        '''
        value = GoogleComputeBackendServiceStrongSessionAffinityCookie(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#create GoogleComputeBackendService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#delete GoogleComputeBackendService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#update GoogleComputeBackendService#update}.
        '''
        value = GoogleComputeBackendServiceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTlsSettings")
    def put_tls_settings(
        self,
        *,
        authentication_config: typing.Optional[builtins.str] = None,
        sni: typing.Optional[builtins.str] = None,
        subject_alt_names: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceTlsSettingsSubjectAltNames", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param authentication_config: Reference to the BackendAuthenticationConfig resource from the networksecurity.googleapis.com namespace. Can be used in authenticating TLS connections to the backend, as specified by the authenticationMode field. Can only be specified if authenticationMode is not NONE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#authentication_config GoogleComputeBackendService#authentication_config}
        :param sni: Server Name Indication - see RFC3546 section 3.1. If set, the load balancer sends this string as the SNI hostname in the TLS connection to the backend, and requires that this string match a Subject Alternative Name (SAN) in the backend's server certificate. With a Regional Internet NEG backend, if the SNI is specified here, the load balancer uses it regardless of whether the Regional Internet NEG is specified with FQDN or IP address and port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#sni GoogleComputeBackendService#sni}
        :param subject_alt_names: subject_alt_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#subject_alt_names GoogleComputeBackendService#subject_alt_names}
        '''
        value = GoogleComputeBackendServiceTlsSettings(
            authentication_config=authentication_config,
            sni=sni,
            subject_alt_names=subject_alt_names,
        )

        return typing.cast(None, jsii.invoke(self, "putTlsSettings", [value]))

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

    @jsii.member(jsii_name="resetCompressionMode")
    def reset_compression_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompressionMode", []))

    @jsii.member(jsii_name="resetConnectionDrainingTimeoutSec")
    def reset_connection_draining_timeout_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionDrainingTimeoutSec", []))

    @jsii.member(jsii_name="resetConsistentHash")
    def reset_consistent_hash(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsistentHash", []))

    @jsii.member(jsii_name="resetCustomMetrics")
    def reset_custom_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomMetrics", []))

    @jsii.member(jsii_name="resetCustomRequestHeaders")
    def reset_custom_request_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRequestHeaders", []))

    @jsii.member(jsii_name="resetCustomResponseHeaders")
    def reset_custom_response_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomResponseHeaders", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDynamicForwarding")
    def reset_dynamic_forwarding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicForwarding", []))

    @jsii.member(jsii_name="resetEdgeSecurityPolicy")
    def reset_edge_security_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeSecurityPolicy", []))

    @jsii.member(jsii_name="resetEnableCdn")
    def reset_enable_cdn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableCdn", []))

    @jsii.member(jsii_name="resetExternalManagedMigrationState")
    def reset_external_managed_migration_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalManagedMigrationState", []))

    @jsii.member(jsii_name="resetExternalManagedMigrationTestingPercentage")
    def reset_external_managed_migration_testing_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalManagedMigrationTestingPercentage", []))

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

    @jsii.member(jsii_name="resetLocalityLbPolicies")
    def reset_locality_lb_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalityLbPolicies", []))

    @jsii.member(jsii_name="resetLocalityLbPolicy")
    def reset_locality_lb_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalityLbPolicy", []))

    @jsii.member(jsii_name="resetLogConfig")
    def reset_log_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogConfig", []))

    @jsii.member(jsii_name="resetMaxStreamDuration")
    def reset_max_stream_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxStreamDuration", []))

    @jsii.member(jsii_name="resetNetworkPassThroughLbTrafficPolicy")
    def reset_network_pass_through_lb_traffic_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkPassThroughLbTrafficPolicy", []))

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

    @jsii.member(jsii_name="resetSecurityPolicy")
    def reset_security_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityPolicy", []))

    @jsii.member(jsii_name="resetSecuritySettings")
    def reset_security_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecuritySettings", []))

    @jsii.member(jsii_name="resetServiceLbPolicy")
    def reset_service_lb_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceLbPolicy", []))

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

    @jsii.member(jsii_name="resetTlsSettings")
    def reset_tls_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsSettings", []))

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
    def backend(self) -> "GoogleComputeBackendServiceBackendList":
        return typing.cast("GoogleComputeBackendServiceBackendList", jsii.get(self, "backend"))

    @builtins.property
    @jsii.member(jsii_name="cdnPolicy")
    def cdn_policy(self) -> "GoogleComputeBackendServiceCdnPolicyOutputReference":
        return typing.cast("GoogleComputeBackendServiceCdnPolicyOutputReference", jsii.get(self, "cdnPolicy"))

    @builtins.property
    @jsii.member(jsii_name="circuitBreakers")
    def circuit_breakers(
        self,
    ) -> "GoogleComputeBackendServiceCircuitBreakersOutputReference":
        return typing.cast("GoogleComputeBackendServiceCircuitBreakersOutputReference", jsii.get(self, "circuitBreakers"))

    @builtins.property
    @jsii.member(jsii_name="consistentHash")
    def consistent_hash(
        self,
    ) -> "GoogleComputeBackendServiceConsistentHashOutputReference":
        return typing.cast("GoogleComputeBackendServiceConsistentHashOutputReference", jsii.get(self, "consistentHash"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="customMetrics")
    def custom_metrics(self) -> "GoogleComputeBackendServiceCustomMetricsList":
        return typing.cast("GoogleComputeBackendServiceCustomMetricsList", jsii.get(self, "customMetrics"))

    @builtins.property
    @jsii.member(jsii_name="dynamicForwarding")
    def dynamic_forwarding(
        self,
    ) -> "GoogleComputeBackendServiceDynamicForwardingOutputReference":
        return typing.cast("GoogleComputeBackendServiceDynamicForwardingOutputReference", jsii.get(self, "dynamicForwarding"))

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
    def iap(self) -> "GoogleComputeBackendServiceIapOutputReference":
        return typing.cast("GoogleComputeBackendServiceIapOutputReference", jsii.get(self, "iap"))

    @builtins.property
    @jsii.member(jsii_name="localityLbPolicies")
    def locality_lb_policies(
        self,
    ) -> "GoogleComputeBackendServiceLocalityLbPoliciesList":
        return typing.cast("GoogleComputeBackendServiceLocalityLbPoliciesList", jsii.get(self, "localityLbPolicies"))

    @builtins.property
    @jsii.member(jsii_name="logConfig")
    def log_config(self) -> "GoogleComputeBackendServiceLogConfigOutputReference":
        return typing.cast("GoogleComputeBackendServiceLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="maxStreamDuration")
    def max_stream_duration(
        self,
    ) -> "GoogleComputeBackendServiceMaxStreamDurationOutputReference":
        return typing.cast("GoogleComputeBackendServiceMaxStreamDurationOutputReference", jsii.get(self, "maxStreamDuration"))

    @builtins.property
    @jsii.member(jsii_name="networkPassThroughLbTrafficPolicy")
    def network_pass_through_lb_traffic_policy(
        self,
    ) -> "GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyOutputReference":
        return typing.cast("GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyOutputReference", jsii.get(self, "networkPassThroughLbTrafficPolicy"))

    @builtins.property
    @jsii.member(jsii_name="outlierDetection")
    def outlier_detection(
        self,
    ) -> "GoogleComputeBackendServiceOutlierDetectionOutputReference":
        return typing.cast("GoogleComputeBackendServiceOutlierDetectionOutputReference", jsii.get(self, "outlierDetection"))

    @builtins.property
    @jsii.member(jsii_name="securitySettings")
    def security_settings(
        self,
    ) -> "GoogleComputeBackendServiceSecuritySettingsOutputReference":
        return typing.cast("GoogleComputeBackendServiceSecuritySettingsOutputReference", jsii.get(self, "securitySettings"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="strongSessionAffinityCookie")
    def strong_session_affinity_cookie(
        self,
    ) -> "GoogleComputeBackendServiceStrongSessionAffinityCookieOutputReference":
        return typing.cast("GoogleComputeBackendServiceStrongSessionAffinityCookieOutputReference", jsii.get(self, "strongSessionAffinityCookie"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleComputeBackendServiceTimeoutsOutputReference":
        return typing.cast("GoogleComputeBackendServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="tlsSettings")
    def tls_settings(self) -> "GoogleComputeBackendServiceTlsSettingsOutputReference":
        return typing.cast("GoogleComputeBackendServiceTlsSettingsOutputReference", jsii.get(self, "tlsSettings"))

    @builtins.property
    @jsii.member(jsii_name="affinityCookieTtlSecInput")
    def affinity_cookie_ttl_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "affinityCookieTtlSecInput"))

    @builtins.property
    @jsii.member(jsii_name="backendInput")
    def backend_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceBackend"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceBackend"]]], jsii.get(self, "backendInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnPolicyInput")
    def cdn_policy_input(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceCdnPolicy"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceCdnPolicy"], jsii.get(self, "cdnPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="circuitBreakersInput")
    def circuit_breakers_input(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceCircuitBreakers"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceCircuitBreakers"], jsii.get(self, "circuitBreakersInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionModeInput")
    def compression_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionDrainingTimeoutSecInput")
    def connection_draining_timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "connectionDrainingTimeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="consistentHashInput")
    def consistent_hash_input(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceConsistentHash"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceConsistentHash"], jsii.get(self, "consistentHashInput"))

    @builtins.property
    @jsii.member(jsii_name="customMetricsInput")
    def custom_metrics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceCustomMetrics"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceCustomMetrics"]]], jsii.get(self, "customMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="customRequestHeadersInput")
    def custom_request_headers_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customRequestHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="customResponseHeadersInput")
    def custom_response_headers_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customResponseHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicForwardingInput")
    def dynamic_forwarding_input(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceDynamicForwarding"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceDynamicForwarding"], jsii.get(self, "dynamicForwardingInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeSecurityPolicyInput")
    def edge_security_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeSecurityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="enableCdnInput")
    def enable_cdn_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableCdnInput"))

    @builtins.property
    @jsii.member(jsii_name="externalManagedMigrationStateInput")
    def external_managed_migration_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalManagedMigrationStateInput"))

    @builtins.property
    @jsii.member(jsii_name="externalManagedMigrationTestingPercentageInput")
    def external_managed_migration_testing_percentage_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "externalManagedMigrationTestingPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="healthChecksInput")
    def health_checks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "healthChecksInput"))

    @builtins.property
    @jsii.member(jsii_name="iapInput")
    def iap_input(self) -> typing.Optional["GoogleComputeBackendServiceIap"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceIap"], jsii.get(self, "iapInput"))

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
    @jsii.member(jsii_name="localityLbPoliciesInput")
    def locality_lb_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceLocalityLbPolicies"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceLocalityLbPolicies"]]], jsii.get(self, "localityLbPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="localityLbPolicyInput")
    def locality_lb_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localityLbPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigInput")
    def log_config_input(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceLogConfig"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceLogConfig"], jsii.get(self, "logConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="maxStreamDurationInput")
    def max_stream_duration_input(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceMaxStreamDuration"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceMaxStreamDuration"], jsii.get(self, "maxStreamDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPassThroughLbTrafficPolicyInput")
    def network_pass_through_lb_traffic_policy_input(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy"], jsii.get(self, "networkPassThroughLbTrafficPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="outlierDetectionInput")
    def outlier_detection_input(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceOutlierDetection"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceOutlierDetection"], jsii.get(self, "outlierDetectionInput"))

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
    @jsii.member(jsii_name="securityPolicyInput")
    def security_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="securitySettingsInput")
    def security_settings_input(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceSecuritySettings"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceSecuritySettings"], jsii.get(self, "securitySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceLbPolicyInput")
    def service_lb_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceLbPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityInput")
    def session_affinity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="strongSessionAffinityCookieInput")
    def strong_session_affinity_cookie_input(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceStrongSessionAffinityCookie"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceStrongSessionAffinityCookie"], jsii.get(self, "strongSessionAffinityCookieInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecInput")
    def timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeBackendServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeBackendServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsSettingsInput")
    def tls_settings_input(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceTlsSettings"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceTlsSettings"], jsii.get(self, "tlsSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="affinityCookieTtlSec")
    def affinity_cookie_ttl_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "affinityCookieTtlSec"))

    @affinity_cookie_ttl_sec.setter
    def affinity_cookie_ttl_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c300e2c4f51f62750e08bb3e2d7fd306c16423de9fa17017095cf9f51137623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "affinityCookieTtlSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="compressionMode")
    def compression_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionMode"))

    @compression_mode.setter
    def compression_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcde712a72bd8b74cd9514a3c0c1bf27306d896885d219eea4f1f5961af1e48c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionDrainingTimeoutSec")
    def connection_draining_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectionDrainingTimeoutSec"))

    @connection_draining_timeout_sec.setter
    def connection_draining_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19bb873284f5b226c661dc1183d8efdb7bee5e57310689e5e24bc55580587497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionDrainingTimeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customRequestHeaders")
    def custom_request_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customRequestHeaders"))

    @custom_request_headers.setter
    def custom_request_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__367e37d76bd7701dd5a09716a160d506a8351643ba61ef77109702ba07a1091a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customRequestHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customResponseHeaders")
    def custom_response_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customResponseHeaders"))

    @custom_response_headers.setter
    def custom_response_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__258c384781e18505ba11ca36a4d6ebacbab2d4c6bc8c239e53346dda882c323e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customResponseHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ba96be69dc0480062569dadc94916e2d321a0bc691c0dfae6642740433abd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgeSecurityPolicy")
    def edge_security_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeSecurityPolicy"))

    @edge_security_policy.setter
    def edge_security_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f974f46a2cd2cfaec39e3d5071fcf1708d32d9391ad2f53a38e8fe1bedc8a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeSecurityPolicy", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__5eb116baaf0206a1ecef7e00495b404e70f4f3b22ecf13a281ab3ddc45c078a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableCdn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalManagedMigrationState")
    def external_managed_migration_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalManagedMigrationState"))

    @external_managed_migration_state.setter
    def external_managed_migration_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdb5248c457bc0a76fead84d2c7e02795b64a867d820d62e44affcf6cc0721a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalManagedMigrationState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalManagedMigrationTestingPercentage")
    def external_managed_migration_testing_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "externalManagedMigrationTestingPercentage"))

    @external_managed_migration_testing_percentage.setter
    def external_managed_migration_testing_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd681836d32e4e8c1b8292d79fc7dd14d086296654349338221783375563b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalManagedMigrationTestingPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthChecks")
    def health_checks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "healthChecks"))

    @health_checks.setter
    def health_checks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20cd214aa6a29f5b36abf3e67990d28c54a84b05d74bbc3538a466798521dee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthChecks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c32e3c06b26ec713d3f43159325889b2a271a835f668fef78d7c959f938e3d3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddressSelectionPolicy")
    def ip_address_selection_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressSelectionPolicy"))

    @ip_address_selection_policy.setter
    def ip_address_selection_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fadcb458461977f9beb50e372ce811e8ab017a32eec95b720b3ef3d74eda022)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressSelectionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingScheme")
    def load_balancing_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingScheme"))

    @load_balancing_scheme.setter
    def load_balancing_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a575ba50772d1d1b473ef0708f05a9477058932bc6f9c5915f06050224a8ef31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingScheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localityLbPolicy")
    def locality_lb_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localityLbPolicy"))

    @locality_lb_policy.setter
    def locality_lb_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db726d683c23ce3f3acfb26b584a0448f10857dfa067d14fed88feb51f55371c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localityLbPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__531ea69a293cb95d2e490c7df74b02f01f69b92d4d372b1886cb4fed488f3561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0492687c02726348a8b5cc110b262b90b07f198fb91e942dd8f10c96bdb33790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b069666c74bf31edd0f973dab2dbec097c78d33f6cc95a6e96e5ad32a0f235c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e0ea2dbcd6666e3e75b86a28118e14169d33c77a7b21f0472858aad708b8d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityPolicy")
    def security_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityPolicy"))

    @security_policy.setter
    def security_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae5abe296333e27f553c8e4cbb7407e02baa10f7a4cfb8d5c001ea64e15662e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceLbPolicy")
    def service_lb_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceLbPolicy"))

    @service_lb_policy.setter
    def service_lb_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a11725d244c105d2224a799fc0dcb1328541ba177df3b101abb4918a624cee2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceLbPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionAffinity")
    def session_affinity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionAffinity"))

    @session_affinity.setter
    def session_affinity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f60b98e55f3a43e5715dbdd9599eba719ffdb5ad4be58e8f6861df7cb158a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSec")
    def timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSec"))

    @timeout_sec.setter
    def timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1bca67a9658007c0f4f10d896c644d2f93122728e16ac28d974baaf42ae2124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSec", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceBackend",
    jsii_struct_bases=[],
    name_mapping={
        "group": "group",
        "balancing_mode": "balancingMode",
        "capacity_scaler": "capacityScaler",
        "custom_metrics": "customMetrics",
        "description": "description",
        "max_connections": "maxConnections",
        "max_connections_per_endpoint": "maxConnectionsPerEndpoint",
        "max_connections_per_instance": "maxConnectionsPerInstance",
        "max_rate": "maxRate",
        "max_rate_per_endpoint": "maxRatePerEndpoint",
        "max_rate_per_instance": "maxRatePerInstance",
        "max_utilization": "maxUtilization",
        "preference": "preference",
    },
)
class GoogleComputeBackendServiceBackend:
    def __init__(
        self,
        *,
        group: builtins.str,
        balancing_mode: typing.Optional[builtins.str] = None,
        capacity_scaler: typing.Optional[jsii.Number] = None,
        custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceBackendCustomMetrics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        max_connections: typing.Optional[jsii.Number] = None,
        max_connections_per_endpoint: typing.Optional[jsii.Number] = None,
        max_connections_per_instance: typing.Optional[jsii.Number] = None,
        max_rate: typing.Optional[jsii.Number] = None,
        max_rate_per_endpoint: typing.Optional[jsii.Number] = None,
        max_rate_per_instance: typing.Optional[jsii.Number] = None,
        max_utilization: typing.Optional[jsii.Number] = None,
        preference: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group: The fully-qualified URL of an Instance Group or Network Endpoint Group resource. In case of instance group this defines the list of instances that serve traffic. Member virtual machine instances from each instance group must live in the same zone as the instance group itself. No two backends in a backend service are allowed to use same Instance Group resource. For Network Endpoint Groups this defines list of endpoints. All endpoints of Network Endpoint Group must be hosted on instances located in the same zone as the Network Endpoint Group. Backend services cannot mix Instance Group and Network Endpoint Group backends. Note that you must specify an Instance Group or Network Endpoint Group resource using the fully-qualified URL, rather than a partial URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#group GoogleComputeBackendService#group}
        :param balancing_mode: Specifies the balancing mode for this backend. For global HTTP(S) or TCP/SSL load balancing, the default is UTILIZATION. Valid values are UTILIZATION, RATE (for HTTP(S)), CUSTOM_METRICS (for HTTP(s)) and CONNECTION (for TCP/SSL). See the `Backend Services Overview <https://cloud.google.com/load-balancing/docs/backend-service#balancing-mode>`_ for an explanation of load balancing modes. Default value: "UTILIZATION" Possible values: ["UTILIZATION", "RATE", "CONNECTION", "CUSTOM_METRICS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#balancing_mode GoogleComputeBackendService#balancing_mode}
        :param capacity_scaler: A multiplier applied to the group's maximum servicing capacity (based on UTILIZATION, RATE or CONNECTION). Default value is 1, which means the group will serve up to 100% of its configured capacity (depending on balancingMode). A setting of 0 means the group is completely drained, offering 0% of its available Capacity. Valid range is [0.0,1.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#capacity_scaler GoogleComputeBackendService#capacity_scaler}
        :param custom_metrics: custom_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#custom_metrics GoogleComputeBackendService#custom_metrics}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#description GoogleComputeBackendService#description}
        :param max_connections: The max number of simultaneous connections for the group. Can be used with either CONNECTION or UTILIZATION balancing modes. For CONNECTION mode, either maxConnections or one of maxConnectionsPerInstance or maxConnectionsPerEndpoint, as appropriate for group type, must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_connections GoogleComputeBackendService#max_connections}
        :param max_connections_per_endpoint: The max number of simultaneous connections that a single backend network endpoint can handle. This is used to calculate the capacity of the group. Can be used in either CONNECTION or UTILIZATION balancing modes. For CONNECTION mode, either maxConnections or maxConnectionsPerEndpoint must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_connections_per_endpoint GoogleComputeBackendService#max_connections_per_endpoint}
        :param max_connections_per_instance: The max number of simultaneous connections that a single backend instance can handle. This is used to calculate the capacity of the group. Can be used in either CONNECTION or UTILIZATION balancing modes. For CONNECTION mode, either maxConnections or maxConnectionsPerInstance must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_connections_per_instance GoogleComputeBackendService#max_connections_per_instance}
        :param max_rate: The max requests per second (RPS) of the group. Can be used with either RATE or UTILIZATION balancing modes, but required if RATE mode. For RATE mode, either maxRate or one of maxRatePerInstance or maxRatePerEndpoint, as appropriate for group type, must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_rate GoogleComputeBackendService#max_rate}
        :param max_rate_per_endpoint: The max requests per second (RPS) that a single backend network endpoint can handle. This is used to calculate the capacity of the group. Can be used in either balancing mode. For RATE mode, either maxRate or maxRatePerEndpoint must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_rate_per_endpoint GoogleComputeBackendService#max_rate_per_endpoint}
        :param max_rate_per_instance: The max requests per second (RPS) that a single backend instance can handle. This is used to calculate the capacity of the group. Can be used in either balancing mode. For RATE mode, either maxRate or maxRatePerInstance must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_rate_per_instance GoogleComputeBackendService#max_rate_per_instance}
        :param max_utilization: Used when balancingMode is UTILIZATION. This ratio defines the CPU utilization target for the group. Valid range is [0.0, 1.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_utilization GoogleComputeBackendService#max_utilization}
        :param preference: This field indicates whether this backend should be fully utilized before sending traffic to backends with default preference. This field cannot be set when loadBalancingScheme is set to 'EXTERNAL'. The possible values are: - PREFERRED: Backends with this preference level will be filled up to their capacity limits first, based on RTT. - DEFAULT: If preferred backends don't have enough capacity, backends in this layer would be used and traffic would be assigned based on the load balancing algorithm you use. This is the default Possible values: ["PREFERRED", "DEFAULT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#preference GoogleComputeBackendService#preference}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efbfd99ae8901f9e57b53eff504b4f7e65974875c7fa4fdabdb38e191a57a736)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument balancing_mode", value=balancing_mode, expected_type=type_hints["balancing_mode"])
            check_type(argname="argument capacity_scaler", value=capacity_scaler, expected_type=type_hints["capacity_scaler"])
            check_type(argname="argument custom_metrics", value=custom_metrics, expected_type=type_hints["custom_metrics"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument max_connections", value=max_connections, expected_type=type_hints["max_connections"])
            check_type(argname="argument max_connections_per_endpoint", value=max_connections_per_endpoint, expected_type=type_hints["max_connections_per_endpoint"])
            check_type(argname="argument max_connections_per_instance", value=max_connections_per_instance, expected_type=type_hints["max_connections_per_instance"])
            check_type(argname="argument max_rate", value=max_rate, expected_type=type_hints["max_rate"])
            check_type(argname="argument max_rate_per_endpoint", value=max_rate_per_endpoint, expected_type=type_hints["max_rate_per_endpoint"])
            check_type(argname="argument max_rate_per_instance", value=max_rate_per_instance, expected_type=type_hints["max_rate_per_instance"])
            check_type(argname="argument max_utilization", value=max_utilization, expected_type=type_hints["max_utilization"])
            check_type(argname="argument preference", value=preference, expected_type=type_hints["preference"])
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
        if preference is not None:
            self._values["preference"] = preference

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

        Note that you must specify an Instance Group or Network Endpoint
        Group resource using the fully-qualified URL, rather than a
        partial URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#group GoogleComputeBackendService#group}
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def balancing_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the balancing mode for this backend.

        For global HTTP(S) or TCP/SSL load balancing, the default is
        UTILIZATION. Valid values are UTILIZATION, RATE (for HTTP(S)),
        CUSTOM_METRICS (for HTTP(s)) and CONNECTION (for TCP/SSL).

        See the `Backend Services Overview <https://cloud.google.com/load-balancing/docs/backend-service#balancing-mode>`_
        for an explanation of load balancing modes. Default value: "UTILIZATION" Possible values: ["UTILIZATION", "RATE", "CONNECTION", "CUSTOM_METRICS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#balancing_mode GoogleComputeBackendService#balancing_mode}
        '''
        result = self._values.get("balancing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def capacity_scaler(self) -> typing.Optional[jsii.Number]:
        '''A multiplier applied to the group's maximum servicing capacity (based on UTILIZATION, RATE or CONNECTION).

        Default value is 1, which means the group will serve up to 100%
        of its configured capacity (depending on balancingMode). A
        setting of 0 means the group is completely drained, offering
        0% of its available Capacity. Valid range is [0.0,1.0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#capacity_scaler GoogleComputeBackendService#capacity_scaler}
        '''
        result = self._values.get("capacity_scaler")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_metrics(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceBackendCustomMetrics"]]]:
        '''custom_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#custom_metrics GoogleComputeBackendService#custom_metrics}
        '''
        result = self._values.get("custom_metrics")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceBackendCustomMetrics"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#description GoogleComputeBackendService#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_connections(self) -> typing.Optional[jsii.Number]:
        '''The max number of simultaneous connections for the group. Can be used with either CONNECTION or UTILIZATION balancing modes.

        For CONNECTION mode, either maxConnections or one
        of maxConnectionsPerInstance or maxConnectionsPerEndpoint,
        as appropriate for group type, must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_connections GoogleComputeBackendService#max_connections}
        '''
        result = self._values.get("max_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_connections_per_endpoint(self) -> typing.Optional[jsii.Number]:
        '''The max number of simultaneous connections that a single backend network endpoint can handle.

        This is used to calculate the
        capacity of the group. Can be used in either CONNECTION or
        UTILIZATION balancing modes.

        For CONNECTION mode, either
        maxConnections or maxConnectionsPerEndpoint must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_connections_per_endpoint GoogleComputeBackendService#max_connections_per_endpoint}
        '''
        result = self._values.get("max_connections_per_endpoint")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_connections_per_instance(self) -> typing.Optional[jsii.Number]:
        '''The max number of simultaneous connections that a single backend instance can handle.

        This is used to calculate the
        capacity of the group. Can be used in either CONNECTION or
        UTILIZATION balancing modes.

        For CONNECTION mode, either maxConnections or
        maxConnectionsPerInstance must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_connections_per_instance GoogleComputeBackendService#max_connections_per_instance}
        '''
        result = self._values.get("max_connections_per_instance")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_rate(self) -> typing.Optional[jsii.Number]:
        '''The max requests per second (RPS) of the group.

        Can be used with either RATE or UTILIZATION balancing modes,
        but required if RATE mode. For RATE mode, either maxRate or one
        of maxRatePerInstance or maxRatePerEndpoint, as appropriate for
        group type, must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_rate GoogleComputeBackendService#max_rate}
        '''
        result = self._values.get("max_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_rate_per_endpoint(self) -> typing.Optional[jsii.Number]:
        '''The max requests per second (RPS) that a single backend network endpoint can handle.

        This is used to calculate the capacity of
        the group. Can be used in either balancing mode. For RATE mode,
        either maxRate or maxRatePerEndpoint must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_rate_per_endpoint GoogleComputeBackendService#max_rate_per_endpoint}
        '''
        result = self._values.get("max_rate_per_endpoint")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_rate_per_instance(self) -> typing.Optional[jsii.Number]:
        '''The max requests per second (RPS) that a single backend instance can handle.

        This is used to calculate the capacity of
        the group. Can be used in either balancing mode. For RATE mode,
        either maxRate or maxRatePerInstance must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_rate_per_instance GoogleComputeBackendService#max_rate_per_instance}
        '''
        result = self._values.get("max_rate_per_instance")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_utilization(self) -> typing.Optional[jsii.Number]:
        '''Used when balancingMode is UTILIZATION. This ratio defines the CPU utilization target for the group. Valid range is [0.0, 1.0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_utilization GoogleComputeBackendService#max_utilization}
        '''
        result = self._values.get("max_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preference(self) -> typing.Optional[builtins.str]:
        '''This field indicates whether this backend should be fully utilized before sending traffic to backends with default preference.

        This field cannot be set when loadBalancingScheme is set to 'EXTERNAL'. The possible values are:

        - PREFERRED: Backends with this preference level will be filled up to their capacity limits first,
          based on RTT.
        - DEFAULT: If preferred backends don't have enough capacity, backends in this layer would be used and
          traffic would be assigned based on the load balancing algorithm you use. This is the default Possible values: ["PREFERRED", "DEFAULT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#preference GoogleComputeBackendService#preference}
        '''
        result = self._values.get("preference")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceBackend(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceBackendCustomMetrics",
    jsii_struct_bases=[],
    name_mapping={
        "dry_run": "dryRun",
        "name": "name",
        "max_utilization": "maxUtilization",
    },
)
class GoogleComputeBackendServiceBackendCustomMetrics:
    def __init__(
        self,
        *,
        dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        max_utilization: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param dry_run: If true, the metric data is collected and reported to Cloud Monitoring, but is not used for load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#dry_run GoogleComputeBackendService#dry_run}
        :param name: Name of a custom utilization signal. The name must be 1-64 characters long and match the regular expression `a-z <%5B-_.a-z0-9%5D*%5Ba-z0-9%5D>`_? which means the first character must be a lowercase letter, and all following characters must be a dash, period, underscore, lowercase letter, or digit, except the last character, which cannot be a dash, period, or underscore. For usage guidelines, see Custom Metrics balancing mode. This field can only be used for a global or regional backend service with the loadBalancingScheme set to EXTERNAL_MANAGED, INTERNAL_MANAGED INTERNAL_SELF_MANAGED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        :param max_utilization: Optional parameter to define a target utilization for the Custom Metrics balancing mode. The valid range is [0.0, 1.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_utilization GoogleComputeBackendService#max_utilization}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a6f1f4f3b9709ec0a7016a77db9a051c35ef00ffffc29a63b03b9387baa845)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#dry_run GoogleComputeBackendService#dry_run}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_utilization(self) -> typing.Optional[jsii.Number]:
        '''Optional parameter to define a target utilization for the Custom Metrics balancing mode. The valid range is [0.0, 1.0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_utilization GoogleComputeBackendService#max_utilization}
        '''
        result = self._values.get("max_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceBackendCustomMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceBackendCustomMetricsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceBackendCustomMetricsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9960907c3c03704fe8de62e01b753009ee4698120b910d8aa074a353c5d830ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeBackendServiceBackendCustomMetricsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b298b6a6768b051b3b424f28531e42f4426113bc8fdb5d56f2d1c6a84a64358d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeBackendServiceBackendCustomMetricsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__578e62076510a8d024f3b3af6e5794d81ab6f03fe3812c507e79dc068b90d247)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61354b978a729701552d5fcaf8649172e663881ed2c7c9d6cc094044827aaed6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11eb0fc2e1f209e75d6bd89735ddb819eef31f936eecf90fb1b1bdb92ba9ddc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceBackendCustomMetrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceBackendCustomMetrics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceBackendCustomMetrics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a765757a197980f30161562769f7bc5045760f6cf0ba271424d47d534083ca6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeBackendServiceBackendCustomMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceBackendCustomMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf1f42b2150ddc108ad1226744f43154871a3d489807b4d394b6d7ea4162610d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9dffeec3cb92d9c84dc3d7cbc08523db2dbe0dc75cc131e112f28b6e7715294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dryRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUtilization")
    def max_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUtilization"))

    @max_utilization.setter
    def max_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2efc037799dcc4035307fbe1530cbb323cb77bb1d2c3a458e4d59683a43671c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96263bdaf506ea81153ea2a1bbaf8b535e534497a36939246f89df0dbab8a0e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceBackendCustomMetrics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceBackendCustomMetrics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceBackendCustomMetrics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4cda6c06f52b533b2c2e246d37d7e7bdaa2df3c1b10c0e40cb3808a815bb5ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeBackendServiceBackendList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceBackendList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b342bbf483acac495c2d0f9488c97f31c747ceeda3a22c789c91af8ba74b5c8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeBackendServiceBackendOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44bbdff86e267f3e46f475381e61bd75f786ceeda155623fd4946805084996a2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeBackendServiceBackendOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e55e4c9e0fa1256d8b974c77beb431005cc8dca53eba70cc5f55e9f2037a1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84ef8031e68e54fb271931f3839f049d634a2b3129e1efb61a862c6b378cc7fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8765e421475e2e13ef2c7db36c13d54a1e34bd71a46e436dc3cb43d044d6f42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceBackend]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceBackend]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceBackend]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc515253954b3ffe3bdc928dc73c2d40154b56156105f21bb51fab026b5c192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeBackendServiceBackendOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceBackendOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6035ac3d4e034391ede18081833c249036b3901c0740592a64b2756216c39f84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomMetrics")
    def put_custom_metrics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceBackendCustomMetrics, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e5efd1f933a766f34c0392287f18d40a9c79382fcf79953b3ac188442008de0)
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

    @jsii.member(jsii_name="resetPreference")
    def reset_preference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreference", []))

    @builtins.property
    @jsii.member(jsii_name="customMetrics")
    def custom_metrics(self) -> GoogleComputeBackendServiceBackendCustomMetricsList:
        return typing.cast(GoogleComputeBackendServiceBackendCustomMetricsList, jsii.get(self, "customMetrics"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceBackendCustomMetrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceBackendCustomMetrics]]], jsii.get(self, "customMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

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
    @jsii.member(jsii_name="preferenceInput")
    def preference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="balancingMode")
    def balancing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "balancingMode"))

    @balancing_mode.setter
    def balancing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b6ed90e5b8342f491d770b546aea83e39537595609aa18ec8ed851bc79fb253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "balancingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capacityScaler")
    def capacity_scaler(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "capacityScaler"))

    @capacity_scaler.setter
    def capacity_scaler(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4085d986ad88d2cfcdc581231c8b4a99c3a1ef63b23badc0595ab127b306aef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityScaler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17515c3740d588a66b894e19e069bac96c0a7cd93f8288b68d25260187e658a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e503fb014457709722374ee1e3a0640bc867df44bae3748b17c1dbc70cedcc36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConnections")
    def max_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnections"))

    @max_connections.setter
    def max_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d80ebbcaedbf05cf5fbdd1ddebedc2ffcc458b8ee30e4c43bd3fae5277d09a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConnectionsPerEndpoint")
    def max_connections_per_endpoint(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionsPerEndpoint"))

    @max_connections_per_endpoint.setter
    def max_connections_per_endpoint(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e563af2b3b783d7599e1ecc968adcab29d590edbf21b5a76be77f0a20b07bdd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionsPerEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConnectionsPerInstance")
    def max_connections_per_instance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionsPerInstance"))

    @max_connections_per_instance.setter
    def max_connections_per_instance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39ce97a2bd93ab69db711ea8dcd9508953e3fc9e0488a918eb96c5da27c5beb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionsPerInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRate")
    def max_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRate"))

    @max_rate.setter
    def max_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d7f801f813229868841647f8a4e936e913bc27f24b3ca4d94a61e27aba8240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRatePerEndpoint")
    def max_rate_per_endpoint(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRatePerEndpoint"))

    @max_rate_per_endpoint.setter
    def max_rate_per_endpoint(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7850419f9cd5380b97178a3fb7a5bf722bf0b22e8cba15a5c924e38390796316)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRatePerEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRatePerInstance")
    def max_rate_per_instance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRatePerInstance"))

    @max_rate_per_instance.setter
    def max_rate_per_instance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed480410089a3ba156071b4b4225480df3b619b92174dcc00d5be46e75d41365)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRatePerInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUtilization")
    def max_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUtilization"))

    @max_utilization.setter
    def max_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5613b2f4b00c7394e1066802026aa16e136341b0dd4f5ed15af1985d8562a69f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preference")
    def preference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preference"))

    @preference.setter
    def preference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be35ed0c847204ded352dfa01a5ba0e12bfe1420f8b186b5f6542a2ebdb0ca70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceBackend]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceBackend]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceBackend]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90239351589195c05b9b256bf3960880113b8d29c97f0126866b9e5f809d9d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCdnPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "bypass_cache_on_request_headers": "bypassCacheOnRequestHeaders",
        "cache_key_policy": "cacheKeyPolicy",
        "cache_mode": "cacheMode",
        "client_ttl": "clientTtl",
        "default_ttl": "defaultTtl",
        "max_ttl": "maxTtl",
        "negative_caching": "negativeCaching",
        "negative_caching_policy": "negativeCachingPolicy",
        "request_coalescing": "requestCoalescing",
        "serve_while_stale": "serveWhileStale",
        "signed_url_cache_max_age_sec": "signedUrlCacheMaxAgeSec",
    },
)
class GoogleComputeBackendServiceCdnPolicy:
    def __init__(
        self,
        *,
        bypass_cache_on_request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cache_key_policy: typing.Optional[typing.Union["GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_mode: typing.Optional[builtins.str] = None,
        client_ttl: typing.Optional[jsii.Number] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        max_ttl: typing.Optional[jsii.Number] = None,
        negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negative_caching_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_coalescing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        serve_while_stale: typing.Optional[jsii.Number] = None,
        signed_url_cache_max_age_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bypass_cache_on_request_headers: bypass_cache_on_request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#bypass_cache_on_request_headers GoogleComputeBackendService#bypass_cache_on_request_headers}
        :param cache_key_policy: cache_key_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#cache_key_policy GoogleComputeBackendService#cache_key_policy}
        :param cache_mode: Specifies the cache setting for all responses from this backend. The possible values are: USE_ORIGIN_HEADERS, FORCE_CACHE_ALL and CACHE_ALL_STATIC Possible values: ["USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "CACHE_ALL_STATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#cache_mode GoogleComputeBackendService#cache_mode}
        :param client_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#client_ttl GoogleComputeBackendService#client_ttl}
        :param default_ttl: Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#default_ttl GoogleComputeBackendService#default_ttl}
        :param max_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_ttl GoogleComputeBackendService#max_ttl}
        :param negative_caching: Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#negative_caching GoogleComputeBackendService#negative_caching}
        :param negative_caching_policy: negative_caching_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#negative_caching_policy GoogleComputeBackendService#negative_caching_policy}
        :param request_coalescing: If true then Cloud CDN will combine multiple concurrent cache fill requests into a small number of requests to the origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#request_coalescing GoogleComputeBackendService#request_coalescing}
        :param serve_while_stale: Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#serve_while_stale GoogleComputeBackendService#serve_while_stale}
        :param signed_url_cache_max_age_sec: Maximum number of seconds the response to a signed URL request will be considered fresh, defaults to 1hr (3600s). After this time period, the response will be revalidated before being served. When serving responses to signed URL requests, Cloud CDN will internally behave as though all responses from this backend had a "Cache-Control: public, max-age=[TTL]" header, regardless of any existing Cache-Control header. The actual headers served in responses will not be altered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#signed_url_cache_max_age_sec GoogleComputeBackendService#signed_url_cache_max_age_sec}
        '''
        if isinstance(cache_key_policy, dict):
            cache_key_policy = GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy(**cache_key_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df2f8d610a7dd12ac6803be451a60d0e7a220ed29b797fae976d0d85e69d4a03)
            check_type(argname="argument bypass_cache_on_request_headers", value=bypass_cache_on_request_headers, expected_type=type_hints["bypass_cache_on_request_headers"])
            check_type(argname="argument cache_key_policy", value=cache_key_policy, expected_type=type_hints["cache_key_policy"])
            check_type(argname="argument cache_mode", value=cache_mode, expected_type=type_hints["cache_mode"])
            check_type(argname="argument client_ttl", value=client_ttl, expected_type=type_hints["client_ttl"])
            check_type(argname="argument default_ttl", value=default_ttl, expected_type=type_hints["default_ttl"])
            check_type(argname="argument max_ttl", value=max_ttl, expected_type=type_hints["max_ttl"])
            check_type(argname="argument negative_caching", value=negative_caching, expected_type=type_hints["negative_caching"])
            check_type(argname="argument negative_caching_policy", value=negative_caching_policy, expected_type=type_hints["negative_caching_policy"])
            check_type(argname="argument request_coalescing", value=request_coalescing, expected_type=type_hints["request_coalescing"])
            check_type(argname="argument serve_while_stale", value=serve_while_stale, expected_type=type_hints["serve_while_stale"])
            check_type(argname="argument signed_url_cache_max_age_sec", value=signed_url_cache_max_age_sec, expected_type=type_hints["signed_url_cache_max_age_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bypass_cache_on_request_headers is not None:
            self._values["bypass_cache_on_request_headers"] = bypass_cache_on_request_headers
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
        if request_coalescing is not None:
            self._values["request_coalescing"] = request_coalescing
        if serve_while_stale is not None:
            self._values["serve_while_stale"] = serve_while_stale
        if signed_url_cache_max_age_sec is not None:
            self._values["signed_url_cache_max_age_sec"] = signed_url_cache_max_age_sec

    @builtins.property
    def bypass_cache_on_request_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders"]]]:
        '''bypass_cache_on_request_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#bypass_cache_on_request_headers GoogleComputeBackendService#bypass_cache_on_request_headers}
        '''
        result = self._values.get("bypass_cache_on_request_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders"]]], result)

    @builtins.property
    def cache_key_policy(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy"]:
        '''cache_key_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#cache_key_policy GoogleComputeBackendService#cache_key_policy}
        '''
        result = self._values.get("cache_key_policy")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy"], result)

    @builtins.property
    def cache_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the cache setting for all responses from this backend.

        The possible values are: USE_ORIGIN_HEADERS, FORCE_CACHE_ALL and CACHE_ALL_STATIC Possible values: ["USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "CACHE_ALL_STATIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#cache_mode GoogleComputeBackendService#cache_mode}
        '''
        result = self._values.get("cache_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_ttl(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum allowed TTL for cached content served by this origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#client_ttl GoogleComputeBackendService#client_ttl}
        '''
        result = self._values.get("client_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_ttl(self) -> typing.Optional[jsii.Number]:
        '''Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#default_ttl GoogleComputeBackendService#default_ttl}
        '''
        result = self._values.get("default_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_ttl(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum allowed TTL for cached content served by this origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_ttl GoogleComputeBackendService#max_ttl}
        '''
        result = self._values.get("max_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def negative_caching(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#negative_caching GoogleComputeBackendService#negative_caching}
        '''
        result = self._values.get("negative_caching")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def negative_caching_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy"]]]:
        '''negative_caching_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#negative_caching_policy GoogleComputeBackendService#negative_caching_policy}
        '''
        result = self._values.get("negative_caching_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy"]]], result)

    @builtins.property
    def request_coalescing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true then Cloud CDN will combine multiple concurrent cache fill requests into a small number of requests to the origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#request_coalescing GoogleComputeBackendService#request_coalescing}
        '''
        result = self._values.get("request_coalescing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def serve_while_stale(self) -> typing.Optional[jsii.Number]:
        '''Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#serve_while_stale GoogleComputeBackendService#serve_while_stale}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#signed_url_cache_max_age_sec GoogleComputeBackendService#signed_url_cache_max_age_sec}
        '''
        result = self._values.get("signed_url_cache_max_age_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceCdnPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName"},
)
class GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders:
    def __init__(self, *, header_name: builtins.str) -> None:
        '''
        :param header_name: The header field name to match on when bypassing cache. Values are case-insensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#header_name GoogleComputeBackendService#header_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ac6ff6712f00660947f24b31de8ffa9af037bc4ecacc35b39ee48080300a4c)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
        }

    @builtins.property
    def header_name(self) -> builtins.str:
        '''The header field name to match on when bypassing cache. Values are case-insensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#header_name GoogleComputeBackendService#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84be7359d11797331c31f0ca67a28670626526d2e9d30ebd314704316f644595)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d889a18c65001ee804c5407422e71a1a84285d4cd79cb82cb48ce2e511001237)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ab94c6c3b544047b0feaa4c44414e5a98e465998f4475e5a08e529fcf4bffa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8162cd9ba39ffd69e774a024269d5e745100c8d634a123b12615af9747dcd4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__370cb7f826b1e427d3adf56e5194b183c3a3498b341e7db8d9b645a63b207d83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca10686008a66fc3e9b75ba11f4a4ac5da0e882856b016e38dba4b8087386f3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb7cea71d5f57e72d1433a2884ab8f5504ec9bd85fee732be49e68ddf0846425)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11e415a66e41e7168c49008ccaf1f9ccb1df036be26a9ca6a01f360469fd965b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d8c1b39a13d5048d9781919f9d7e9f29955e55bf63423272d532aaa46edb9f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "include_host": "includeHost",
        "include_http_headers": "includeHttpHeaders",
        "include_named_cookies": "includeNamedCookies",
        "include_protocol": "includeProtocol",
        "include_query_string": "includeQueryString",
        "query_string_blacklist": "queryStringBlacklist",
        "query_string_whitelist": "queryStringWhitelist",
    },
)
class GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy:
    def __init__(
        self,
        *,
        include_host: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_http_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_named_cookies: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_protocol: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_query_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_string_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param include_host: If true requests to different hosts will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#include_host GoogleComputeBackendService#include_host}
        :param include_http_headers: Allows HTTP request headers (by name) to be used in the cache key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#include_http_headers GoogleComputeBackendService#include_http_headers}
        :param include_named_cookies: Names of cookies to include in cache keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#include_named_cookies GoogleComputeBackendService#include_named_cookies}
        :param include_protocol: If true, http and https requests will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#include_protocol GoogleComputeBackendService#include_protocol}
        :param include_query_string: If true, include query string parameters in the cache key according to query_string_whitelist and query_string_blacklist. If neither is set, the entire query string will be included. If false, the query string will be excluded from the cache key entirely. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#include_query_string GoogleComputeBackendService#include_query_string}
        :param query_string_blacklist: Names of query string parameters to exclude in cache keys. All other parameters will be included. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#query_string_blacklist GoogleComputeBackendService#query_string_blacklist}
        :param query_string_whitelist: Names of query string parameters to include in cache keys. All other parameters will be excluded. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#query_string_whitelist GoogleComputeBackendService#query_string_whitelist}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99f91c7c73ed77a18f0de68ad6213b196a738c65e436ee5165db7323e5a1df89)
            check_type(argname="argument include_host", value=include_host, expected_type=type_hints["include_host"])
            check_type(argname="argument include_http_headers", value=include_http_headers, expected_type=type_hints["include_http_headers"])
            check_type(argname="argument include_named_cookies", value=include_named_cookies, expected_type=type_hints["include_named_cookies"])
            check_type(argname="argument include_protocol", value=include_protocol, expected_type=type_hints["include_protocol"])
            check_type(argname="argument include_query_string", value=include_query_string, expected_type=type_hints["include_query_string"])
            check_type(argname="argument query_string_blacklist", value=query_string_blacklist, expected_type=type_hints["query_string_blacklist"])
            check_type(argname="argument query_string_whitelist", value=query_string_whitelist, expected_type=type_hints["query_string_whitelist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if include_host is not None:
            self._values["include_host"] = include_host
        if include_http_headers is not None:
            self._values["include_http_headers"] = include_http_headers
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#include_host GoogleComputeBackendService#include_host}
        '''
        result = self._values.get("include_host")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_http_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Allows HTTP request headers (by name) to be used in the cache key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#include_http_headers GoogleComputeBackendService#include_http_headers}
        '''
        result = self._values.get("include_http_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_named_cookies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of cookies to include in cache keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#include_named_cookies GoogleComputeBackendService#include_named_cookies}
        '''
        result = self._values.get("include_named_cookies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, http and https requests will be cached separately.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#include_protocol GoogleComputeBackendService#include_protocol}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#include_query_string GoogleComputeBackendService#include_query_string}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#query_string_blacklist GoogleComputeBackendService#query_string_blacklist}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#query_string_whitelist GoogleComputeBackendService#query_string_whitelist}
        '''
        result = self._values.get("query_string_whitelist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceCdnPolicyCacheKeyPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCdnPolicyCacheKeyPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acfd96ca8aaae016391bd054c8f4c5fe9a4044bc1c11344d588d1e3ed1f175b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeHost")
    def reset_include_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeHost", []))

    @jsii.member(jsii_name="resetIncludeHttpHeaders")
    def reset_include_http_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeHttpHeaders", []))

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
    @jsii.member(jsii_name="includeHttpHeadersInput")
    def include_http_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeHttpHeadersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__269c3523464835a9509500bae8114aedca719a0f0dbbb36d75ccdb402d0e7c91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeHttpHeaders")
    def include_http_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeHttpHeaders"))

    @include_http_headers.setter
    def include_http_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78cc6e9790b96cc5f6e889833cc1cd39d5047f5176faeca527cfd73816a9e0a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeHttpHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeNamedCookies")
    def include_named_cookies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeNamedCookies"))

    @include_named_cookies.setter
    def include_named_cookies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b047faab6949c5aa771b2b12f8bdbc97972d2e187fc6689f1720c89c97952b0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cb9487a45303a0314c9956d0e80cd20beefc6a966abbe3c73773937b718df60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d296cca71448a3b351787399d4f1aebff0ae0a3bb760537a34c450ecaccc14f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeQueryString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringBlacklist")
    def query_string_blacklist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryStringBlacklist"))

    @query_string_blacklist.setter
    def query_string_blacklist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea889fbb303af93e913f48d85e08c83d37b29c7bd3d76cbb884f0a0b437d829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringBlacklist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringWhitelist")
    def query_string_whitelist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryStringWhitelist"))

    @query_string_whitelist.setter
    def query_string_whitelist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046572159bc53e0243661a621902305a5d21e8a06ed2eff14049bed9c656fdf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringWhitelist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb55b8d4d60a41a5f969e06cd470e1a4874915e9226a4b2f6353d16b725e376c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy",
    jsii_struct_bases=[],
    name_mapping={"code": "code", "ttl": "ttl"},
)
class GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy:
    def __init__(
        self,
        *,
        code: typing.Optional[jsii.Number] = None,
        ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param code: The HTTP status code to define a TTL against. Only HTTP status codes 300, 301, 308, 404, 405, 410, 421, 451 and 501 can be specified as values, and you cannot specify a status code more than once. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#code GoogleComputeBackendService#code}
        :param ttl: The TTL (in seconds) for which to cache responses with the corresponding status code. The maximum allowed value is 1800s (30 minutes), noting that infrequently accessed objects may be evicted from the cache before the defined TTL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#ttl GoogleComputeBackendService#ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c74ed9a1649bebae85c400edc899582035d138c5aa97f2b04b08bb8060fcc3f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#code GoogleComputeBackendService#code}
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''The TTL (in seconds) for which to cache responses with the corresponding status code.

        The maximum allowed value is 1800s
        (30 minutes), noting that infrequently accessed objects may be evicted from the cache before the defined TTL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#ttl GoogleComputeBackendService#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5b93c6aad0c0d07cd01145bd38ea2af98d1c61842369cba178d97c4afffb896)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0689d2fb6a4c146b46902281572f28a698316aa413a2980d0a9194d57fa2977)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d2c133203ce230d525c6dd1d8e6099af683b62b85d16650dd7fca68af3074f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e276a2a62c2b234b283fe888d7fe5f5d52dd44dc222d75353aacad8c17cca2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63da294d021fa65bc5869637eedf4addf6550d5f640315dddd6022d201f8241d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa4309394517fee8e849dbf9cef59f0e7eb5ccb235ab8ac519c0d4d5f91f7781)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__971bb0642d515d2ef6cab1f24c8aceac3b8b7938d2848b07fd98213c22dc8e5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c72c9b43b3829daa79cd9938d903d18870a7d69cd938bde70d91106a448f7c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e720ebc76f05ffcb84824a230db7bcdf7242d34fa0be3d3c84fc130ca2f15524)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37cec9c185a1985f3bb0745543060b4bc3a67ee1fcf0966f105b3582c7a5fe1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeBackendServiceCdnPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCdnPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f10d3c5efc43305b60008988789e35b8a80507c801acaf6f0d5f2f8f4f4fac81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBypassCacheOnRequestHeaders")
    def put_bypass_cache_on_request_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07da1a7e6f32856bfae2ed793e5b1d1c25f642e8b46662de3220f5edd42556ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBypassCacheOnRequestHeaders", [value]))

    @jsii.member(jsii_name="putCacheKeyPolicy")
    def put_cache_key_policy(
        self,
        *,
        include_host: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_http_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_named_cookies: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_protocol: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_query_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_string_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param include_host: If true requests to different hosts will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#include_host GoogleComputeBackendService#include_host}
        :param include_http_headers: Allows HTTP request headers (by name) to be used in the cache key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#include_http_headers GoogleComputeBackendService#include_http_headers}
        :param include_named_cookies: Names of cookies to include in cache keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#include_named_cookies GoogleComputeBackendService#include_named_cookies}
        :param include_protocol: If true, http and https requests will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#include_protocol GoogleComputeBackendService#include_protocol}
        :param include_query_string: If true, include query string parameters in the cache key according to query_string_whitelist and query_string_blacklist. If neither is set, the entire query string will be included. If false, the query string will be excluded from the cache key entirely. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#include_query_string GoogleComputeBackendService#include_query_string}
        :param query_string_blacklist: Names of query string parameters to exclude in cache keys. All other parameters will be included. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#query_string_blacklist GoogleComputeBackendService#query_string_blacklist}
        :param query_string_whitelist: Names of query string parameters to include in cache keys. All other parameters will be excluded. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#query_string_whitelist GoogleComputeBackendService#query_string_whitelist}
        '''
        value = GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy(
            include_host=include_host,
            include_http_headers=include_http_headers,
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e5a3a815228ecfaa8d6940c776e06ee53a15c1b602e18a353b4254fd98e0076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNegativeCachingPolicy", [value]))

    @jsii.member(jsii_name="resetBypassCacheOnRequestHeaders")
    def reset_bypass_cache_on_request_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBypassCacheOnRequestHeaders", []))

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

    @jsii.member(jsii_name="resetRequestCoalescing")
    def reset_request_coalescing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestCoalescing", []))

    @jsii.member(jsii_name="resetServeWhileStale")
    def reset_serve_while_stale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServeWhileStale", []))

    @jsii.member(jsii_name="resetSignedUrlCacheMaxAgeSec")
    def reset_signed_url_cache_max_age_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignedUrlCacheMaxAgeSec", []))

    @builtins.property
    @jsii.member(jsii_name="bypassCacheOnRequestHeaders")
    def bypass_cache_on_request_headers(
        self,
    ) -> GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersList:
        return typing.cast(GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersList, jsii.get(self, "bypassCacheOnRequestHeaders"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyPolicy")
    def cache_key_policy(
        self,
    ) -> GoogleComputeBackendServiceCdnPolicyCacheKeyPolicyOutputReference:
        return typing.cast(GoogleComputeBackendServiceCdnPolicyCacheKeyPolicyOutputReference, jsii.get(self, "cacheKeyPolicy"))

    @builtins.property
    @jsii.member(jsii_name="negativeCachingPolicy")
    def negative_caching_policy(
        self,
    ) -> GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicyList:
        return typing.cast(GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicyList, jsii.get(self, "negativeCachingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="bypassCacheOnRequestHeadersInput")
    def bypass_cache_on_request_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]]], jsii.get(self, "bypassCacheOnRequestHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyPolicyInput")
    def cache_key_policy_input(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy], jsii.get(self, "cacheKeyPolicyInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy]]], jsii.get(self, "negativeCachingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="requestCoalescingInput")
    def request_coalescing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requestCoalescingInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__517d2102abafd2cc81339ecbb54d8152c53e4c200d6e2d8b537413b7f1fb5ea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTtl")
    def client_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientTtl"))

    @client_ttl.setter
    def client_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d06cc68283b754add3fcf7935676826df90ca6c60ebb65814f456de603e9cd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db3e312030792fd997f09e30024112d9467eb8139d1bf62acb66fe5399035071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTtl")
    def max_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxTtl"))

    @max_ttl.setter
    def max_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0bceea232334d511832d4e2fae3e11e5dd94cbccf076df2c011c5646ad24c43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8dd85234b72580be5b11f1098fbceead6b51508ddf453552fb5e05b14275fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negativeCaching", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestCoalescing")
    def request_coalescing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requestCoalescing"))

    @request_coalescing.setter
    def request_coalescing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3addb66014d29faaf83451e8dd1fdd0099a21c475798fbb34fcf23448dda177e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestCoalescing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serveWhileStale")
    def serve_while_stale(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "serveWhileStale"))

    @serve_while_stale.setter
    def serve_while_stale(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d096cb83cc27e6a72d15c6563c0a357e03366811663d421be1a6f96f9b1ba02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serveWhileStale", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signedUrlCacheMaxAgeSec")
    def signed_url_cache_max_age_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "signedUrlCacheMaxAgeSec"))

    @signed_url_cache_max_age_sec.setter
    def signed_url_cache_max_age_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624f6d17f505d469677ed77ebb6efbff1c0c1ed4c7aa91dd1b175380d8eb8043)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signedUrlCacheMaxAgeSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComputeBackendServiceCdnPolicy]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceCdnPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceCdnPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__730760ef13ac64964461c8e9181fed8329cbfeb7f4e7d51194611ab2f0ff8498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCircuitBreakers",
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
class GoogleComputeBackendServiceCircuitBreakers:
    def __init__(
        self,
        *,
        connect_timeout: typing.Optional[typing.Union["GoogleComputeBackendServiceCircuitBreakersConnectTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
        max_connections: typing.Optional[jsii.Number] = None,
        max_pending_requests: typing.Optional[jsii.Number] = None,
        max_requests: typing.Optional[jsii.Number] = None,
        max_requests_per_connection: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connect_timeout: connect_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#connect_timeout GoogleComputeBackendService#connect_timeout}
        :param max_connections: The maximum number of connections to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_connections GoogleComputeBackendService#max_connections}
        :param max_pending_requests: The maximum number of pending requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_pending_requests GoogleComputeBackendService#max_pending_requests}
        :param max_requests: The maximum number of parallel requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_requests GoogleComputeBackendService#max_requests}
        :param max_requests_per_connection: Maximum requests for a single backend connection. This parameter is respected by both the HTTP/1.1 and HTTP/2 implementations. If not specified, there is no limit. Setting this parameter to 1 will effectively disable keep alive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_requests_per_connection GoogleComputeBackendService#max_requests_per_connection}
        :param max_retries: The maximum number of parallel retries to the backend cluster. Defaults to 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_retries GoogleComputeBackendService#max_retries}
        '''
        if isinstance(connect_timeout, dict):
            connect_timeout = GoogleComputeBackendServiceCircuitBreakersConnectTimeout(**connect_timeout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ddd4c95c404355b1ccf2493eeabb1575b9411b5b898cbec0412b975305346e)
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
    ) -> typing.Optional["GoogleComputeBackendServiceCircuitBreakersConnectTimeout"]:
        '''connect_timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#connect_timeout GoogleComputeBackendService#connect_timeout}
        '''
        result = self._values.get("connect_timeout")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceCircuitBreakersConnectTimeout"], result)

    @builtins.property
    def max_connections(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of connections to the backend cluster. Defaults to 1024.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_connections GoogleComputeBackendService#max_connections}
        '''
        result = self._values.get("max_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_pending_requests(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of pending requests to the backend cluster. Defaults to 1024.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_pending_requests GoogleComputeBackendService#max_pending_requests}
        '''
        result = self._values.get("max_pending_requests")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_requests(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of parallel requests to the backend cluster. Defaults to 1024.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_requests GoogleComputeBackendService#max_requests}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_requests_per_connection GoogleComputeBackendService#max_requests_per_connection}
        '''
        result = self._values.get("max_requests_per_connection")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of parallel retries to the backend cluster. Defaults to 3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_retries GoogleComputeBackendService#max_retries}
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceCircuitBreakers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCircuitBreakersConnectTimeout",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class GoogleComputeBackendServiceCircuitBreakersConnectTimeout:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35d2532f0077c762a6af1f071e70525c6930fde0841abc941a1d9e00e1541bc9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceCircuitBreakersConnectTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceCircuitBreakersConnectTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCircuitBreakersConnectTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a02802aa3a1adcc3dc53b0abe1d2930c46e424d48805d2005f281285376c0ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbf6bfd6c7d8aa557f2226b2c06a74e31bce189c3b143f6c46edb370e3e12384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecc9491401f47b70933ce79267543a58216e35e8464de2c124917b677f892d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceCircuitBreakersConnectTimeout]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceCircuitBreakersConnectTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceCircuitBreakersConnectTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24c63a4e2de79fe986d02eb915986f8bfbf96894242688ee4696344670d07382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeBackendServiceCircuitBreakersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCircuitBreakersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b1515814a18c4f8e25e4ff9241dc6e7a5389534d75e473b28a6d2d258afea5d)
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        value = GoogleComputeBackendServiceCircuitBreakersConnectTimeout(
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
    ) -> GoogleComputeBackendServiceCircuitBreakersConnectTimeoutOutputReference:
        return typing.cast(GoogleComputeBackendServiceCircuitBreakersConnectTimeoutOutputReference, jsii.get(self, "connectTimeout"))

    @builtins.property
    @jsii.member(jsii_name="connectTimeoutInput")
    def connect_timeout_input(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceCircuitBreakersConnectTimeout]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceCircuitBreakersConnectTimeout], jsii.get(self, "connectTimeoutInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__582b88cc5855defa1573babe95685ca0c4db2687a38522d6514bdb4c208dfc77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPendingRequests")
    def max_pending_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPendingRequests"))

    @max_pending_requests.setter
    def max_pending_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0cd8eb54d7bc0d34daa42c95cbd3cf7c1918b2828b56fab3fd4ec02262c492)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPendingRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRequests")
    def max_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRequests"))

    @max_requests.setter
    def max_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1501b33ac78fbdc1a94099e32e63eb8b5cf5d9c7f43c36221e8282995f35d185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRequestsPerConnection")
    def max_requests_per_connection(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRequestsPerConnection"))

    @max_requests_per_connection.setter
    def max_requests_per_connection(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__247a2d7ab5f986c85e353009408e0b61ab29ca4394785671bc901dc507397182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRequestsPerConnection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df499aa6d1f06db0729cb4fac6e0cf295d99245c40077e524a9b8b2b52f354ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceCircuitBreakers]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceCircuitBreakers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceCircuitBreakers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f923395fbe7a9531935d66e17285cb71c20f4dce6b7ab2d9e90ac7bf1a0d190a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceConfig",
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
        "compression_mode": "compressionMode",
        "connection_draining_timeout_sec": "connectionDrainingTimeoutSec",
        "consistent_hash": "consistentHash",
        "custom_metrics": "customMetrics",
        "custom_request_headers": "customRequestHeaders",
        "custom_response_headers": "customResponseHeaders",
        "description": "description",
        "dynamic_forwarding": "dynamicForwarding",
        "edge_security_policy": "edgeSecurityPolicy",
        "enable_cdn": "enableCdn",
        "external_managed_migration_state": "externalManagedMigrationState",
        "external_managed_migration_testing_percentage": "externalManagedMigrationTestingPercentage",
        "health_checks": "healthChecks",
        "iap": "iap",
        "id": "id",
        "ip_address_selection_policy": "ipAddressSelectionPolicy",
        "load_balancing_scheme": "loadBalancingScheme",
        "locality_lb_policies": "localityLbPolicies",
        "locality_lb_policy": "localityLbPolicy",
        "log_config": "logConfig",
        "max_stream_duration": "maxStreamDuration",
        "network_pass_through_lb_traffic_policy": "networkPassThroughLbTrafficPolicy",
        "outlier_detection": "outlierDetection",
        "port_name": "portName",
        "project": "project",
        "protocol": "protocol",
        "security_policy": "securityPolicy",
        "security_settings": "securitySettings",
        "service_lb_policy": "serviceLbPolicy",
        "session_affinity": "sessionAffinity",
        "strong_session_affinity_cookie": "strongSessionAffinityCookie",
        "timeouts": "timeouts",
        "timeout_sec": "timeoutSec",
        "tls_settings": "tlsSettings",
    },
)
class GoogleComputeBackendServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cdn_policy: typing.Optional[typing.Union[GoogleComputeBackendServiceCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        circuit_breakers: typing.Optional[typing.Union[GoogleComputeBackendServiceCircuitBreakers, typing.Dict[builtins.str, typing.Any]]] = None,
        compression_mode: typing.Optional[builtins.str] = None,
        connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
        consistent_hash: typing.Optional[typing.Union["GoogleComputeBackendServiceConsistentHash", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceCustomMetrics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_request_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_response_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamic_forwarding: typing.Optional[typing.Union["GoogleComputeBackendServiceDynamicForwarding", typing.Dict[builtins.str, typing.Any]]] = None,
        edge_security_policy: typing.Optional[builtins.str] = None,
        enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_managed_migration_state: typing.Optional[builtins.str] = None,
        external_managed_migration_testing_percentage: typing.Optional[jsii.Number] = None,
        health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        iap: typing.Optional[typing.Union["GoogleComputeBackendServiceIap", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address_selection_policy: typing.Optional[builtins.str] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        locality_lb_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceLocalityLbPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        locality_lb_policy: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["GoogleComputeBackendServiceLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        max_stream_duration: typing.Optional[typing.Union["GoogleComputeBackendServiceMaxStreamDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        network_pass_through_lb_traffic_policy: typing.Optional[typing.Union["GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        outlier_detection: typing.Optional[typing.Union["GoogleComputeBackendServiceOutlierDetection", typing.Dict[builtins.str, typing.Any]]] = None,
        port_name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        security_policy: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[typing.Union["GoogleComputeBackendServiceSecuritySettings", typing.Dict[builtins.str, typing.Any]]] = None,
        service_lb_policy: typing.Optional[builtins.str] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        strong_session_affinity_cookie: typing.Optional[typing.Union["GoogleComputeBackendServiceStrongSessionAffinityCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeBackendServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_sec: typing.Optional[jsii.Number] = None,
        tls_settings: typing.Optional[typing.Union["GoogleComputeBackendServiceTlsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        :param affinity_cookie_ttl_sec: Lifetime of cookies in seconds if session_affinity is GENERATED_COOKIE. If set to 0, the cookie is non-persistent and lasts only until the end of the browser session (or equivalent). The maximum allowed value for TTL is one day. When the load balancing scheme is INTERNAL, this field is not used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#affinity_cookie_ttl_sec GoogleComputeBackendService#affinity_cookie_ttl_sec}
        :param backend: backend block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#backend GoogleComputeBackendService#backend}
        :param cdn_policy: cdn_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#cdn_policy GoogleComputeBackendService#cdn_policy}
        :param circuit_breakers: circuit_breakers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#circuit_breakers GoogleComputeBackendService#circuit_breakers}
        :param compression_mode: Compress text responses using Brotli or gzip compression, based on the client's Accept-Encoding header. Possible values: ["AUTOMATIC", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#compression_mode GoogleComputeBackendService#compression_mode}
        :param connection_draining_timeout_sec: Time for which instance will be drained (not accept new connections, but still work to finish started). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#connection_draining_timeout_sec GoogleComputeBackendService#connection_draining_timeout_sec}
        :param consistent_hash: consistent_hash block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#consistent_hash GoogleComputeBackendService#consistent_hash}
        :param custom_metrics: custom_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#custom_metrics GoogleComputeBackendService#custom_metrics}
        :param custom_request_headers: Headers that the HTTP/S load balancer should add to proxied requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#custom_request_headers GoogleComputeBackendService#custom_request_headers}
        :param custom_response_headers: Headers that the HTTP/S load balancer should add to proxied responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#custom_response_headers GoogleComputeBackendService#custom_response_headers}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#description GoogleComputeBackendService#description}
        :param dynamic_forwarding: dynamic_forwarding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#dynamic_forwarding GoogleComputeBackendService#dynamic_forwarding}
        :param edge_security_policy: The resource URL for the edge security policy associated with this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#edge_security_policy GoogleComputeBackendService#edge_security_policy}
        :param enable_cdn: If true, enable Cloud CDN for this BackendService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enable_cdn GoogleComputeBackendService#enable_cdn}
        :param external_managed_migration_state: Specifies the canary migration state. Possible values are PREPARE, TEST_BY_PERCENTAGE, and TEST_ALL_TRAFFIC. To begin the migration from EXTERNAL to EXTERNAL_MANAGED, the state must be changed to PREPARE. The state must be changed to TEST_ALL_TRAFFIC before the loadBalancingScheme can be changed to EXTERNAL_MANAGED. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate traffic by percentage using externalManagedMigrationTestingPercentage. Rolling back a migration requires the states to be set in reverse order. So changing the scheme from EXTERNAL_MANAGED to EXTERNAL requires the state to be set to TEST_ALL_TRAFFIC at the same time. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate some traffic back to EXTERNAL or PREPARE can be used to migrate all traffic back to EXTERNAL. Possible values: ["PREPARE", "TEST_BY_PERCENTAGE", "TEST_ALL_TRAFFIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#external_managed_migration_state GoogleComputeBackendService#external_managed_migration_state}
        :param external_managed_migration_testing_percentage: Determines the fraction of requests that should be processed by the Global external Application Load Balancer. The value of this field must be in the range [0, 100]. Session affinity options will slightly affect this routing behavior, for more details, see: Session Affinity. This value can only be set if the loadBalancingScheme in the backend service is set to EXTERNAL (when using the Classic ALB) and the migration state is TEST_BY_PERCENTAGE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#external_managed_migration_testing_percentage GoogleComputeBackendService#external_managed_migration_testing_percentage}
        :param health_checks: The set of URLs to the HttpHealthCheck or HttpsHealthCheck resource for health checking this BackendService. Currently at most one health check can be specified. A health check must be specified unless the backend service uses an internet or serverless NEG as a backend. For internal load balancing, a URL to a HealthCheck resource must be specified instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#health_checks GoogleComputeBackendService#health_checks}
        :param iap: iap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#iap GoogleComputeBackendService#iap}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#id GoogleComputeBackendService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address_selection_policy: Specifies preference of traffic to the backend (from the proxy and from the client for proxyless gRPC). Possible values: ["IPV4_ONLY", "PREFER_IPV6", "IPV6_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#ip_address_selection_policy GoogleComputeBackendService#ip_address_selection_policy}
        :param load_balancing_scheme: Indicates whether the backend service will be used with internal or external load balancing. A backend service created for one type of load balancing cannot be used with the other. For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "INTERNAL_SELF_MANAGED", "INTERNAL_MANAGED", "EXTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#load_balancing_scheme GoogleComputeBackendService#load_balancing_scheme}
        :param locality_lb_policies: locality_lb_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#locality_lb_policies GoogleComputeBackendService#locality_lb_policies}
        :param locality_lb_policy: The load balancing algorithm used within the scope of the locality. The possible values are:. - 'ROUND_ROBIN': This is a simple policy in which each healthy backend is selected in round robin order. - 'LEAST_REQUEST': An O(1) algorithm which selects two random healthy hosts and picks the host which has fewer active requests. - 'RING_HASH': The ring/modulo hash load balancer implements consistent hashing to backends. The algorithm has the property that the addition/removal of a host from a set of N hosts only affects 1/N of the requests. - 'RANDOM': The load balancer selects a random healthy host. - 'ORIGINAL_DESTINATION': Backend host is selected based on the client connection metadata, i.e., connections are opened to the same address as the destination address of the incoming connection before the connection was redirected to the load balancer. - 'MAGLEV': used as a drop in replacement for the ring hash load balancer. Maglev is not as stable as ring hash but has faster table lookup build times and host selection times. For more information about Maglev, refer to https://ai.google/research/pubs/pub44824 - 'WEIGHTED_MAGLEV': Per-instance weighted Load Balancing via health check reported weights. Only applicable to loadBalancingScheme EXTERNAL. If set, the Backend Service must configure a non legacy HTTP-based Health Check, and health check replies are expected to contain non-standard HTTP response header field X-Load-Balancing-Endpoint-Weight to specify the per-instance weights. If set, Load Balancing is weight based on the per-instance weights reported in the last processed health check replies, as long as every instance either reported a valid weight or had UNAVAILABLE_WEIGHT. Otherwise, Load Balancing remains equal-weight. - 'WEIGHTED_ROUND_ROBIN': Per-endpoint weighted round-robin Load Balancing using weights computed from Backend reported Custom Metrics. If set, the Backend Service responses are expected to contain non-standard HTTP response header field X-Endpoint-Load-Metrics. The reported metrics to use for computing the weights are specified via the backends[].customMetrics fields. locality_lb_policy is applicable to either: - A regional backend service with the service_protocol set to HTTP, HTTPS, HTTP2 or H2C, and loadBalancingScheme set to INTERNAL_MANAGED. - A global backend service with the load_balancing_scheme set to INTERNAL_SELF_MANAGED. - A regional backend service with loadBalancingScheme set to EXTERNAL (External Network Load Balancing). Only MAGLEV and WEIGHTED_MAGLEV values are possible for External Network Load Balancing. The default is MAGLEV. If session_affinity is not NONE, and locality_lb_policy is not set to MAGLEV, WEIGHTED_MAGLEV, or RING_HASH, session affinity settings will not take effect. Only ROUND_ROBIN and RING_HASH are supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validate_for_proxyless field set to true. Possible values: ["ROUND_ROBIN", "LEAST_REQUEST", "RING_HASH", "RANDOM", "ORIGINAL_DESTINATION", "MAGLEV", "WEIGHTED_MAGLEV", "WEIGHTED_ROUND_ROBIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#locality_lb_policy GoogleComputeBackendService#locality_lb_policy}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#log_config GoogleComputeBackendService#log_config}
        :param max_stream_duration: max_stream_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_stream_duration GoogleComputeBackendService#max_stream_duration}
        :param network_pass_through_lb_traffic_policy: network_pass_through_lb_traffic_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#network_pass_through_lb_traffic_policy GoogleComputeBackendService#network_pass_through_lb_traffic_policy}
        :param outlier_detection: outlier_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#outlier_detection GoogleComputeBackendService#outlier_detection}
        :param port_name: Name of backend port. The same name should appear in the instance groups referenced by this service. Required when the load balancing scheme is EXTERNAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#port_name GoogleComputeBackendService#port_name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#project GoogleComputeBackendService#project}.
        :param protocol: The protocol this BackendService uses to communicate with backends. The default is HTTP. Possible values are HTTP, HTTPS, HTTP2, H2C, TCP, SSL, UDP or GRPC. Refer to the documentation for the load balancers or for Traffic Director for more information. Must be set to GRPC when the backend service is referenced by a URL map that is bound to target gRPC proxy. Possible values: ["HTTP", "HTTPS", "HTTP2", "TCP", "SSL", "UDP", "GRPC", "UNSPECIFIED", "H2C"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#protocol GoogleComputeBackendService#protocol}
        :param security_policy: The security policy associated with this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#security_policy GoogleComputeBackendService#security_policy}
        :param security_settings: security_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#security_settings GoogleComputeBackendService#security_settings}
        :param service_lb_policy: URL to networkservices.ServiceLbPolicy resource. Can only be set if load balancing scheme is EXTERNAL, EXTERNAL_MANAGED, INTERNAL_MANAGED or INTERNAL_SELF_MANAGED and the scope is global. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#service_lb_policy GoogleComputeBackendService#service_lb_policy}
        :param session_affinity: Type of session affinity to use. The default is NONE. Session affinity is not applicable if the protocol is UDP. Possible values: ["NONE", "CLIENT_IP", "CLIENT_IP_PORT_PROTO", "CLIENT_IP_PROTO", "GENERATED_COOKIE", "HEADER_FIELD", "HTTP_COOKIE", "STRONG_COOKIE_AFFINITY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#session_affinity GoogleComputeBackendService#session_affinity}
        :param strong_session_affinity_cookie: strong_session_affinity_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#strong_session_affinity_cookie GoogleComputeBackendService#strong_session_affinity_cookie}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#timeouts GoogleComputeBackendService#timeouts}
        :param timeout_sec: The backend service timeout has a different meaning depending on the type of load balancer. For more information see, `Backend service settings <https://cloud.google.com/compute/docs/reference/rest/v1/backendServices>`_. The default is 30 seconds. The full range of timeout values allowed goes from 1 through 2,147,483,647 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#timeout_sec GoogleComputeBackendService#timeout_sec}
        :param tls_settings: tls_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#tls_settings GoogleComputeBackendService#tls_settings}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cdn_policy, dict):
            cdn_policy = GoogleComputeBackendServiceCdnPolicy(**cdn_policy)
        if isinstance(circuit_breakers, dict):
            circuit_breakers = GoogleComputeBackendServiceCircuitBreakers(**circuit_breakers)
        if isinstance(consistent_hash, dict):
            consistent_hash = GoogleComputeBackendServiceConsistentHash(**consistent_hash)
        if isinstance(dynamic_forwarding, dict):
            dynamic_forwarding = GoogleComputeBackendServiceDynamicForwarding(**dynamic_forwarding)
        if isinstance(iap, dict):
            iap = GoogleComputeBackendServiceIap(**iap)
        if isinstance(log_config, dict):
            log_config = GoogleComputeBackendServiceLogConfig(**log_config)
        if isinstance(max_stream_duration, dict):
            max_stream_duration = GoogleComputeBackendServiceMaxStreamDuration(**max_stream_duration)
        if isinstance(network_pass_through_lb_traffic_policy, dict):
            network_pass_through_lb_traffic_policy = GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy(**network_pass_through_lb_traffic_policy)
        if isinstance(outlier_detection, dict):
            outlier_detection = GoogleComputeBackendServiceOutlierDetection(**outlier_detection)
        if isinstance(security_settings, dict):
            security_settings = GoogleComputeBackendServiceSecuritySettings(**security_settings)
        if isinstance(strong_session_affinity_cookie, dict):
            strong_session_affinity_cookie = GoogleComputeBackendServiceStrongSessionAffinityCookie(**strong_session_affinity_cookie)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeBackendServiceTimeouts(**timeouts)
        if isinstance(tls_settings, dict):
            tls_settings = GoogleComputeBackendServiceTlsSettings(**tls_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed14fbb2abe53b9f287310fcd21c391043238e9e7bc9962b07467d23228cd710)
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
            check_type(argname="argument compression_mode", value=compression_mode, expected_type=type_hints["compression_mode"])
            check_type(argname="argument connection_draining_timeout_sec", value=connection_draining_timeout_sec, expected_type=type_hints["connection_draining_timeout_sec"])
            check_type(argname="argument consistent_hash", value=consistent_hash, expected_type=type_hints["consistent_hash"])
            check_type(argname="argument custom_metrics", value=custom_metrics, expected_type=type_hints["custom_metrics"])
            check_type(argname="argument custom_request_headers", value=custom_request_headers, expected_type=type_hints["custom_request_headers"])
            check_type(argname="argument custom_response_headers", value=custom_response_headers, expected_type=type_hints["custom_response_headers"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dynamic_forwarding", value=dynamic_forwarding, expected_type=type_hints["dynamic_forwarding"])
            check_type(argname="argument edge_security_policy", value=edge_security_policy, expected_type=type_hints["edge_security_policy"])
            check_type(argname="argument enable_cdn", value=enable_cdn, expected_type=type_hints["enable_cdn"])
            check_type(argname="argument external_managed_migration_state", value=external_managed_migration_state, expected_type=type_hints["external_managed_migration_state"])
            check_type(argname="argument external_managed_migration_testing_percentage", value=external_managed_migration_testing_percentage, expected_type=type_hints["external_managed_migration_testing_percentage"])
            check_type(argname="argument health_checks", value=health_checks, expected_type=type_hints["health_checks"])
            check_type(argname="argument iap", value=iap, expected_type=type_hints["iap"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_address_selection_policy", value=ip_address_selection_policy, expected_type=type_hints["ip_address_selection_policy"])
            check_type(argname="argument load_balancing_scheme", value=load_balancing_scheme, expected_type=type_hints["load_balancing_scheme"])
            check_type(argname="argument locality_lb_policies", value=locality_lb_policies, expected_type=type_hints["locality_lb_policies"])
            check_type(argname="argument locality_lb_policy", value=locality_lb_policy, expected_type=type_hints["locality_lb_policy"])
            check_type(argname="argument log_config", value=log_config, expected_type=type_hints["log_config"])
            check_type(argname="argument max_stream_duration", value=max_stream_duration, expected_type=type_hints["max_stream_duration"])
            check_type(argname="argument network_pass_through_lb_traffic_policy", value=network_pass_through_lb_traffic_policy, expected_type=type_hints["network_pass_through_lb_traffic_policy"])
            check_type(argname="argument outlier_detection", value=outlier_detection, expected_type=type_hints["outlier_detection"])
            check_type(argname="argument port_name", value=port_name, expected_type=type_hints["port_name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
            check_type(argname="argument security_settings", value=security_settings, expected_type=type_hints["security_settings"])
            check_type(argname="argument service_lb_policy", value=service_lb_policy, expected_type=type_hints["service_lb_policy"])
            check_type(argname="argument session_affinity", value=session_affinity, expected_type=type_hints["session_affinity"])
            check_type(argname="argument strong_session_affinity_cookie", value=strong_session_affinity_cookie, expected_type=type_hints["strong_session_affinity_cookie"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument timeout_sec", value=timeout_sec, expected_type=type_hints["timeout_sec"])
            check_type(argname="argument tls_settings", value=tls_settings, expected_type=type_hints["tls_settings"])
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
        if compression_mode is not None:
            self._values["compression_mode"] = compression_mode
        if connection_draining_timeout_sec is not None:
            self._values["connection_draining_timeout_sec"] = connection_draining_timeout_sec
        if consistent_hash is not None:
            self._values["consistent_hash"] = consistent_hash
        if custom_metrics is not None:
            self._values["custom_metrics"] = custom_metrics
        if custom_request_headers is not None:
            self._values["custom_request_headers"] = custom_request_headers
        if custom_response_headers is not None:
            self._values["custom_response_headers"] = custom_response_headers
        if description is not None:
            self._values["description"] = description
        if dynamic_forwarding is not None:
            self._values["dynamic_forwarding"] = dynamic_forwarding
        if edge_security_policy is not None:
            self._values["edge_security_policy"] = edge_security_policy
        if enable_cdn is not None:
            self._values["enable_cdn"] = enable_cdn
        if external_managed_migration_state is not None:
            self._values["external_managed_migration_state"] = external_managed_migration_state
        if external_managed_migration_testing_percentage is not None:
            self._values["external_managed_migration_testing_percentage"] = external_managed_migration_testing_percentage
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
        if locality_lb_policies is not None:
            self._values["locality_lb_policies"] = locality_lb_policies
        if locality_lb_policy is not None:
            self._values["locality_lb_policy"] = locality_lb_policy
        if log_config is not None:
            self._values["log_config"] = log_config
        if max_stream_duration is not None:
            self._values["max_stream_duration"] = max_stream_duration
        if network_pass_through_lb_traffic_policy is not None:
            self._values["network_pass_through_lb_traffic_policy"] = network_pass_through_lb_traffic_policy
        if outlier_detection is not None:
            self._values["outlier_detection"] = outlier_detection
        if port_name is not None:
            self._values["port_name"] = port_name
        if project is not None:
            self._values["project"] = project
        if protocol is not None:
            self._values["protocol"] = protocol
        if security_policy is not None:
            self._values["security_policy"] = security_policy
        if security_settings is not None:
            self._values["security_settings"] = security_settings
        if service_lb_policy is not None:
            self._values["service_lb_policy"] = service_lb_policy
        if session_affinity is not None:
            self._values["session_affinity"] = session_affinity
        if strong_session_affinity_cookie is not None:
            self._values["strong_session_affinity_cookie"] = strong_session_affinity_cookie
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if timeout_sec is not None:
            self._values["timeout_sec"] = timeout_sec
        if tls_settings is not None:
            self._values["tls_settings"] = tls_settings

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#affinity_cookie_ttl_sec GoogleComputeBackendService#affinity_cookie_ttl_sec}
        '''
        result = self._values.get("affinity_cookie_ttl_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def backend(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceBackend]]]:
        '''backend block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#backend GoogleComputeBackendService#backend}
        '''
        result = self._values.get("backend")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceBackend]]], result)

    @builtins.property
    def cdn_policy(self) -> typing.Optional[GoogleComputeBackendServiceCdnPolicy]:
        '''cdn_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#cdn_policy GoogleComputeBackendService#cdn_policy}
        '''
        result = self._values.get("cdn_policy")
        return typing.cast(typing.Optional[GoogleComputeBackendServiceCdnPolicy], result)

    @builtins.property
    def circuit_breakers(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceCircuitBreakers]:
        '''circuit_breakers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#circuit_breakers GoogleComputeBackendService#circuit_breakers}
        '''
        result = self._values.get("circuit_breakers")
        return typing.cast(typing.Optional[GoogleComputeBackendServiceCircuitBreakers], result)

    @builtins.property
    def compression_mode(self) -> typing.Optional[builtins.str]:
        '''Compress text responses using Brotli or gzip compression, based on the client's Accept-Encoding header. Possible values: ["AUTOMATIC", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#compression_mode GoogleComputeBackendService#compression_mode}
        '''
        result = self._values.get("compression_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_draining_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Time for which instance will be drained (not accept new connections, but still work to finish started).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#connection_draining_timeout_sec GoogleComputeBackendService#connection_draining_timeout_sec}
        '''
        result = self._values.get("connection_draining_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def consistent_hash(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceConsistentHash"]:
        '''consistent_hash block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#consistent_hash GoogleComputeBackendService#consistent_hash}
        '''
        result = self._values.get("consistent_hash")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceConsistentHash"], result)

    @builtins.property
    def custom_metrics(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceCustomMetrics"]]]:
        '''custom_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#custom_metrics GoogleComputeBackendService#custom_metrics}
        '''
        result = self._values.get("custom_metrics")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceCustomMetrics"]]], result)

    @builtins.property
    def custom_request_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Headers that the HTTP/S load balancer should add to proxied requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#custom_request_headers GoogleComputeBackendService#custom_request_headers}
        '''
        result = self._values.get("custom_request_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def custom_response_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Headers that the HTTP/S load balancer should add to proxied responses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#custom_response_headers GoogleComputeBackendService#custom_response_headers}
        '''
        result = self._values.get("custom_response_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#description GoogleComputeBackendService#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamic_forwarding(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceDynamicForwarding"]:
        '''dynamic_forwarding block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#dynamic_forwarding GoogleComputeBackendService#dynamic_forwarding}
        '''
        result = self._values.get("dynamic_forwarding")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceDynamicForwarding"], result)

    @builtins.property
    def edge_security_policy(self) -> typing.Optional[builtins.str]:
        '''The resource URL for the edge security policy associated with this backend service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#edge_security_policy GoogleComputeBackendService#edge_security_policy}
        '''
        result = self._values.get("edge_security_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_cdn(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, enable Cloud CDN for this BackendService.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enable_cdn GoogleComputeBackendService#enable_cdn}
        '''
        result = self._values.get("enable_cdn")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def external_managed_migration_state(self) -> typing.Optional[builtins.str]:
        '''Specifies the canary migration state. Possible values are PREPARE, TEST_BY_PERCENTAGE, and TEST_ALL_TRAFFIC.

        To begin the migration from EXTERNAL to EXTERNAL_MANAGED, the state must be changed to
        PREPARE. The state must be changed to TEST_ALL_TRAFFIC before the loadBalancingScheme can be
        changed to EXTERNAL_MANAGED. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate
        traffic by percentage using externalManagedMigrationTestingPercentage.

        Rolling back a migration requires the states to be set in reverse order. So changing the
        scheme from EXTERNAL_MANAGED to EXTERNAL requires the state to be set to TEST_ALL_TRAFFIC at
        the same time. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate some traffic
        back to EXTERNAL or PREPARE can be used to migrate all traffic back to EXTERNAL. Possible values: ["PREPARE", "TEST_BY_PERCENTAGE", "TEST_ALL_TRAFFIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#external_managed_migration_state GoogleComputeBackendService#external_managed_migration_state}
        '''
        result = self._values.get("external_managed_migration_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_managed_migration_testing_percentage(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Determines the fraction of requests that should be processed by the Global external Application Load Balancer.

        The value of this field must be in the range [0, 100].

        Session affinity options will slightly affect this routing behavior, for more details,
        see: Session Affinity.

        This value can only be set if the loadBalancingScheme in the backend service is set to
        EXTERNAL (when using the Classic ALB) and the migration state is TEST_BY_PERCENTAGE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#external_managed_migration_testing_percentage GoogleComputeBackendService#external_managed_migration_testing_percentage}
        '''
        result = self._values.get("external_managed_migration_testing_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_checks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of URLs to the HttpHealthCheck or HttpsHealthCheck resource for health checking this BackendService.

        Currently at most one health
        check can be specified.

        A health check must be specified unless the backend service uses an internet
        or serverless NEG as a backend.

        For internal load balancing, a URL to a HealthCheck resource must be specified instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#health_checks GoogleComputeBackendService#health_checks}
        '''
        result = self._values.get("health_checks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def iap(self) -> typing.Optional["GoogleComputeBackendServiceIap"]:
        '''iap block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#iap GoogleComputeBackendService#iap}
        '''
        result = self._values.get("iap")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceIap"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#id GoogleComputeBackendService#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address_selection_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies preference of traffic to the backend (from the proxy and from the client for proxyless gRPC).

        Possible values: ["IPV4_ONLY", "PREFER_IPV6", "IPV6_ONLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#ip_address_selection_policy GoogleComputeBackendService#ip_address_selection_policy}
        '''
        result = self._values.get("ip_address_selection_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancing_scheme(self) -> typing.Optional[builtins.str]:
        '''Indicates whether the backend service will be used with internal or external load balancing.

        A backend service created for one type of
        load balancing cannot be used with the other. For more information, refer to
        `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "INTERNAL_SELF_MANAGED", "INTERNAL_MANAGED", "EXTERNAL_MANAGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#load_balancing_scheme GoogleComputeBackendService#load_balancing_scheme}
        '''
        result = self._values.get("load_balancing_scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locality_lb_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceLocalityLbPolicies"]]]:
        '''locality_lb_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#locality_lb_policies GoogleComputeBackendService#locality_lb_policies}
        '''
        result = self._values.get("locality_lb_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceLocalityLbPolicies"]]], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#locality_lb_policy GoogleComputeBackendService#locality_lb_policy}
        '''
        result = self._values.get("locality_lb_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_config(self) -> typing.Optional["GoogleComputeBackendServiceLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#log_config GoogleComputeBackendService#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceLogConfig"], result)

    @builtins.property
    def max_stream_duration(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceMaxStreamDuration"]:
        '''max_stream_duration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_stream_duration GoogleComputeBackendService#max_stream_duration}
        '''
        result = self._values.get("max_stream_duration")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceMaxStreamDuration"], result)

    @builtins.property
    def network_pass_through_lb_traffic_policy(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy"]:
        '''network_pass_through_lb_traffic_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#network_pass_through_lb_traffic_policy GoogleComputeBackendService#network_pass_through_lb_traffic_policy}
        '''
        result = self._values.get("network_pass_through_lb_traffic_policy")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy"], result)

    @builtins.property
    def outlier_detection(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceOutlierDetection"]:
        '''outlier_detection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#outlier_detection GoogleComputeBackendService#outlier_detection}
        '''
        result = self._values.get("outlier_detection")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceOutlierDetection"], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Name of backend port.

        The same name should appear in the instance
        groups referenced by this service. Required when the load balancing
        scheme is EXTERNAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#port_name GoogleComputeBackendService#port_name}
        '''
        result = self._values.get("port_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#project GoogleComputeBackendService#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol this BackendService uses to communicate with backends.

        The default is HTTP. Possible values are HTTP, HTTPS, HTTP2, H2C, TCP, SSL, UDP
        or GRPC. Refer to the documentation for the load balancers or for Traffic Director
        for more information. Must be set to GRPC when the backend service is referenced
        by a URL map that is bound to target gRPC proxy. Possible values: ["HTTP", "HTTPS", "HTTP2", "TCP", "SSL", "UDP", "GRPC", "UNSPECIFIED", "H2C"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#protocol GoogleComputeBackendService#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_policy(self) -> typing.Optional[builtins.str]:
        '''The security policy associated with this backend service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#security_policy GoogleComputeBackendService#security_policy}
        '''
        result = self._values.get("security_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_settings(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceSecuritySettings"]:
        '''security_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#security_settings GoogleComputeBackendService#security_settings}
        '''
        result = self._values.get("security_settings")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceSecuritySettings"], result)

    @builtins.property
    def service_lb_policy(self) -> typing.Optional[builtins.str]:
        '''URL to networkservices.ServiceLbPolicy resource. Can only be set if load balancing scheme is EXTERNAL, EXTERNAL_MANAGED, INTERNAL_MANAGED or INTERNAL_SELF_MANAGED and the scope is global.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#service_lb_policy GoogleComputeBackendService#service_lb_policy}
        '''
        result = self._values.get("service_lb_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_affinity(self) -> typing.Optional[builtins.str]:
        '''Type of session affinity to use.

        The default is NONE. Session affinity is
        not applicable if the protocol is UDP. Possible values: ["NONE", "CLIENT_IP", "CLIENT_IP_PORT_PROTO", "CLIENT_IP_PROTO", "GENERATED_COOKIE", "HEADER_FIELD", "HTTP_COOKIE", "STRONG_COOKIE_AFFINITY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#session_affinity GoogleComputeBackendService#session_affinity}
        '''
        result = self._values.get("session_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strong_session_affinity_cookie(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceStrongSessionAffinityCookie"]:
        '''strong_session_affinity_cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#strong_session_affinity_cookie GoogleComputeBackendService#strong_session_affinity_cookie}
        '''
        result = self._values.get("strong_session_affinity_cookie")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceStrongSessionAffinityCookie"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeBackendServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#timeouts GoogleComputeBackendService#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceTimeouts"], result)

    @builtins.property
    def timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''The backend service timeout has a different meaning depending on the type of load balancer.

        For more information see, `Backend service settings <https://cloud.google.com/compute/docs/reference/rest/v1/backendServices>`_.
        The default is 30 seconds.
        The full range of timeout values allowed goes from 1 through 2,147,483,647 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#timeout_sec GoogleComputeBackendService#timeout_sec}
        '''
        result = self._values.get("timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tls_settings(self) -> typing.Optional["GoogleComputeBackendServiceTlsSettings"]:
        '''tls_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#tls_settings GoogleComputeBackendService#tls_settings}
        '''
        result = self._values.get("tls_settings")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceTlsSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceConsistentHash",
    jsii_struct_bases=[],
    name_mapping={
        "http_cookie": "httpCookie",
        "http_header_name": "httpHeaderName",
        "minimum_ring_size": "minimumRingSize",
    },
)
class GoogleComputeBackendServiceConsistentHash:
    def __init__(
        self,
        *,
        http_cookie: typing.Optional[typing.Union["GoogleComputeBackendServiceConsistentHashHttpCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        http_header_name: typing.Optional[builtins.str] = None,
        minimum_ring_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_cookie: http_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#http_cookie GoogleComputeBackendService#http_cookie}
        :param http_header_name: The hash based on the value of the specified header field. This field is applicable if the sessionAffinity is set to HEADER_FIELD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#http_header_name GoogleComputeBackendService#http_header_name}
        :param minimum_ring_size: The minimum number of virtual nodes to use for the hash ring. Larger ring sizes result in more granular load distributions. If the number of hosts in the load balancing pool is larger than the ring size, each host will be assigned a single virtual node. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#minimum_ring_size GoogleComputeBackendService#minimum_ring_size}
        '''
        if isinstance(http_cookie, dict):
            http_cookie = GoogleComputeBackendServiceConsistentHashHttpCookie(**http_cookie)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47ed398189a17dd18841f7f40edd00fb2d882f2bef6d6b8fbc80916bf142337)
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
    ) -> typing.Optional["GoogleComputeBackendServiceConsistentHashHttpCookie"]:
        '''http_cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#http_cookie GoogleComputeBackendService#http_cookie}
        '''
        result = self._values.get("http_cookie")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceConsistentHashHttpCookie"], result)

    @builtins.property
    def http_header_name(self) -> typing.Optional[builtins.str]:
        '''The hash based on the value of the specified header field.

        This field is applicable if the sessionAffinity is set to HEADER_FIELD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#http_header_name GoogleComputeBackendService#http_header_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#minimum_ring_size GoogleComputeBackendService#minimum_ring_size}
        '''
        result = self._values.get("minimum_ring_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceConsistentHash(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceConsistentHashHttpCookie",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "ttl": "ttl"},
)
class GoogleComputeBackendServiceConsistentHashHttpCookie:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[typing.Union["GoogleComputeBackendServiceConsistentHashHttpCookieTtl", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#path GoogleComputeBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#ttl GoogleComputeBackendService#ttl}
        '''
        if isinstance(ttl, dict):
            ttl = GoogleComputeBackendServiceConsistentHashHttpCookieTtl(**ttl)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0272d3f5627409ca8472996cf123061117bfc99a58951e4c4ebe882a5a52e72c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to set for the cookie.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#path GoogleComputeBackendService#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceConsistentHashHttpCookieTtl"]:
        '''ttl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#ttl GoogleComputeBackendService#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceConsistentHashHttpCookieTtl"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceConsistentHashHttpCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceConsistentHashHttpCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceConsistentHashHttpCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d511ae43f272b0e25004df9b862cfc235233a0dad3383f334478d52d8d349e3)
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        value = GoogleComputeBackendServiceConsistentHashHttpCookieTtl(
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
    ) -> "GoogleComputeBackendServiceConsistentHashHttpCookieTtlOutputReference":
        return typing.cast("GoogleComputeBackendServiceConsistentHashHttpCookieTtlOutputReference", jsii.get(self, "ttl"))

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
    ) -> typing.Optional["GoogleComputeBackendServiceConsistentHashHttpCookieTtl"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceConsistentHashHttpCookieTtl"], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7208c4548dbd9fd3c27fbbda160531eef612002dae4ce84b107a865fac216f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96729fcd20bfea86177bf99d88570a6b349cd153848c9073ced8af1cf6602820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceConsistentHashHttpCookie]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceConsistentHashHttpCookie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceConsistentHashHttpCookie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9ed96aa5eab76e1561d9c90b71490cb95574b9f539e600f6937a4c1ebdd4106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceConsistentHashHttpCookieTtl",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class GoogleComputeBackendServiceConsistentHashHttpCookieTtl:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__330ccd7c72b76e1018e602374d0d4254b54584a6ea295860ef9d38955a82c32c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceConsistentHashHttpCookieTtl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceConsistentHashHttpCookieTtlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceConsistentHashHttpCookieTtlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcbeb89629142d46d3103b466dcfdde501a3e6c0285f62b9e4f7cd2f4b7fc423)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97070570a117c24be6e0af083be9cf4d80101839f1ccbd4a45d634be0be8979f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__654fcbf254b2ddd28bcc2124b72588a327c33f3fec185531e97bca0fe037ce53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceConsistentHashHttpCookieTtl]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceConsistentHashHttpCookieTtl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceConsistentHashHttpCookieTtl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b1274dac7201ff51667bdcf48d6f8905b7fe71c79a2bb62d6b2cbe6dc94aa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeBackendServiceConsistentHashOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceConsistentHashOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad1addd16f254248f4a269859d6754925e36c340f23ed3bf5f096285ccda07c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpCookie")
    def put_http_cookie(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[typing.Union[GoogleComputeBackendServiceConsistentHashHttpCookieTtl, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#path GoogleComputeBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#ttl GoogleComputeBackendService#ttl}
        '''
        value = GoogleComputeBackendServiceConsistentHashHttpCookie(
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
    ) -> GoogleComputeBackendServiceConsistentHashHttpCookieOutputReference:
        return typing.cast(GoogleComputeBackendServiceConsistentHashHttpCookieOutputReference, jsii.get(self, "httpCookie"))

    @builtins.property
    @jsii.member(jsii_name="httpCookieInput")
    def http_cookie_input(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceConsistentHashHttpCookie]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceConsistentHashHttpCookie], jsii.get(self, "httpCookieInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2c270f3df8ebe44bf8195f9d8c38cfbd49a47cd695d837e335d9f7e4477387f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumRingSize")
    def minimum_ring_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumRingSize"))

    @minimum_ring_size.setter
    def minimum_ring_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c07d401d9b283640cf447b05ea553c35e634c0c7618b02bf79b6a1e763af70f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumRingSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceConsistentHash]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceConsistentHash], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceConsistentHash],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e5bee1008f896b5454c65f5baab95c83810152dea6982fc8beecb9c7b7e0b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCustomMetrics",
    jsii_struct_bases=[],
    name_mapping={"dry_run": "dryRun", "name": "name"},
)
class GoogleComputeBackendServiceCustomMetrics:
    def __init__(
        self,
        *,
        dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
    ) -> None:
        '''
        :param dry_run: If true, the metric data is not used for load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#dry_run GoogleComputeBackendService#dry_run}
        :param name: Name of a custom utilization signal. The name must be 1-64 characters long and match the regular expression `a-z <%5B-_.a-z0-9%5D*%5Ba-z0-9%5D>`_? which means the first character must be a lowercase letter, and all following characters must be a dash, period, underscore, lowercase letter, or digit, except the last character, which cannot be a dash, period, or underscore. For usage guidelines, see Custom Metrics balancing mode. This field can only be used for a global or regional backend service with the loadBalancingScheme set to EXTERNAL_MANAGED, INTERNAL_MANAGED INTERNAL_SELF_MANAGED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21caebe388725dc872106446bd88c969a3ebaf6ac6b3a4370158cb8eda0828c5)
            check_type(argname="argument dry_run", value=dry_run, expected_type=type_hints["dry_run"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dry_run": dry_run,
            "name": name,
        }

    @builtins.property
    def dry_run(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, the metric data is not used for load balancing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#dry_run GoogleComputeBackendService#dry_run}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceCustomMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceCustomMetricsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCustomMetricsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b53b99188e767122950eabafb030fadc086fa5924b466201bdacd5ec9640330a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeBackendServiceCustomMetricsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90edac07746f5bdbae4395a39de27078ac3d3788732fb2d36e3bca2246c3c36b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeBackendServiceCustomMetricsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24545f976bdcacc2fdeedd4dedc472a115aa68ac5e1732cb12090bfb1021c6e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b873e1a91e5c6c1631ceab9d51c7d9c1378c9e83a22fe364dfecc16247922ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0731b21e12abe3489add56f226cfd6763a855b8b4968c6e83d1bf3043226ffa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCustomMetrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCustomMetrics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCustomMetrics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4e2716c397f72c64e89d3018c03545d8ffc1de08ea5ed061ad481d549ddeda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeBackendServiceCustomMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceCustomMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07f445adb205d7a6b32f609e380ed4423b5854ce262a349f091e33c2f9e4c8ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd0500b7eb6493f66540b442437329f3b0a90f1653b1e13b49b62e3c37c33e1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dryRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e45bc4b3d31136fca224c7e8a7d35e6192d65b0a75b326d047a8866d1edb9dbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceCustomMetrics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceCustomMetrics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceCustomMetrics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__399e9923df24b22feb284b0f8b74aee218572d5bd59619aa6d61047845a3f922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceDynamicForwarding",
    jsii_struct_bases=[],
    name_mapping={"ip_port_selection": "ipPortSelection"},
)
class GoogleComputeBackendServiceDynamicForwarding:
    def __init__(
        self,
        *,
        ip_port_selection: typing.Optional[typing.Union["GoogleComputeBackendServiceDynamicForwardingIpPortSelection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ip_port_selection: ip_port_selection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#ip_port_selection GoogleComputeBackendService#ip_port_selection}
        '''
        if isinstance(ip_port_selection, dict):
            ip_port_selection = GoogleComputeBackendServiceDynamicForwardingIpPortSelection(**ip_port_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3381437c9f16150ea171c867a5b2548ca4204c6b2f8fe2bfeb5479cd2a681169)
            check_type(argname="argument ip_port_selection", value=ip_port_selection, expected_type=type_hints["ip_port_selection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ip_port_selection is not None:
            self._values["ip_port_selection"] = ip_port_selection

    @builtins.property
    def ip_port_selection(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceDynamicForwardingIpPortSelection"]:
        '''ip_port_selection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#ip_port_selection GoogleComputeBackendService#ip_port_selection}
        '''
        result = self._values.get("ip_port_selection")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceDynamicForwardingIpPortSelection"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceDynamicForwarding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceDynamicForwardingIpPortSelection",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleComputeBackendServiceDynamicForwardingIpPortSelection:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: A boolean flag enabling IP:PORT based dynamic forwarding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enabled GoogleComputeBackendService#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395fd8e4734db8b7d226b281732500662906a229429395097325b8c50d035bd5)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean flag enabling IP:PORT based dynamic forwarding.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enabled GoogleComputeBackendService#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceDynamicForwardingIpPortSelection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceDynamicForwardingIpPortSelectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceDynamicForwardingIpPortSelectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__327917f90ffb6107496fdba67eb5756a62e6d27d70d55810eede752a4c3a5b91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be473ba8bd849695e2570f9428fcab49c2989df539c8abae9aaa176a28d03160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceDynamicForwardingIpPortSelection]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceDynamicForwardingIpPortSelection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceDynamicForwardingIpPortSelection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ebc0294dc64b37b397e83cdd566fce84b6922e04d2226709f02293af8a06a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeBackendServiceDynamicForwardingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceDynamicForwardingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f62e7e0070b9f20920932e2d19c2bd70c1e2ad872d6e35f9ab05bbd7e86dfda0)
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
        :param enabled: A boolean flag enabling IP:PORT based dynamic forwarding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enabled GoogleComputeBackendService#enabled}
        '''
        value = GoogleComputeBackendServiceDynamicForwardingIpPortSelection(
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
    ) -> GoogleComputeBackendServiceDynamicForwardingIpPortSelectionOutputReference:
        return typing.cast(GoogleComputeBackendServiceDynamicForwardingIpPortSelectionOutputReference, jsii.get(self, "ipPortSelection"))

    @builtins.property
    @jsii.member(jsii_name="ipPortSelectionInput")
    def ip_port_selection_input(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceDynamicForwardingIpPortSelection]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceDynamicForwardingIpPortSelection], jsii.get(self, "ipPortSelectionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceDynamicForwarding]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceDynamicForwarding], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceDynamicForwarding],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d768f6adcb50f55b5d7bdd4db35943c8d821ce37bc72017ca6c28cb8d4cf0a75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceIap",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "oauth2_client_id": "oauth2ClientId",
        "oauth2_client_secret": "oauth2ClientSecret",
    },
)
class GoogleComputeBackendServiceIap:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        oauth2_client_id: typing.Optional[builtins.str] = None,
        oauth2_client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Whether the serving infrastructure will authenticate and authorize all incoming requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enabled GoogleComputeBackendService#enabled}
        :param oauth2_client_id: OAuth2 Client ID for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#oauth2_client_id GoogleComputeBackendService#oauth2_client_id}
        :param oauth2_client_secret: OAuth2 Client Secret for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#oauth2_client_secret GoogleComputeBackendService#oauth2_client_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__120f433cf9d7c6dc483a77a37580b5ba640af33aed515c15ff21140a4f836997)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enabled GoogleComputeBackendService#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def oauth2_client_id(self) -> typing.Optional[builtins.str]:
        '''OAuth2 Client ID for IAP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#oauth2_client_id GoogleComputeBackendService#oauth2_client_id}
        '''
        result = self._values.get("oauth2_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth2_client_secret(self) -> typing.Optional[builtins.str]:
        '''OAuth2 Client Secret for IAP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#oauth2_client_secret GoogleComputeBackendService#oauth2_client_secret}
        '''
        result = self._values.get("oauth2_client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceIap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceIapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceIapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__379ad90dab79269c462c528995eb5295da18b9064ab1c14032d9f0b164b895b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d611178e7af931cea04a624a86449f45bba959d03b8f9e878c04b5a334b867b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientId")
    def oauth2_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2ClientId"))

    @oauth2_client_id.setter
    def oauth2_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6012b6f127e0a20ec7a9697824ca0ef01205ac2f6d4501c3cd0096de8e8989a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauth2ClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientSecret")
    def oauth2_client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2ClientSecret"))

    @oauth2_client_secret.setter
    def oauth2_client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__806a62e749148a71abad5018e841827adbdfce1ffb5094cb5eff731be21116d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauth2ClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComputeBackendServiceIap]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceIap], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceIap],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e76a17569c941f9e8ea3a3f5c1099326483cb2ca1046551ba911f6bec3bd2cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceLocalityLbPolicies",
    jsii_struct_bases=[],
    name_mapping={"custom_policy": "customPolicy", "policy": "policy"},
)
class GoogleComputeBackendServiceLocalityLbPolicies:
    def __init__(
        self,
        *,
        custom_policy: typing.Optional[typing.Union["GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        policy: typing.Optional[typing.Union["GoogleComputeBackendServiceLocalityLbPoliciesPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_policy: custom_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#custom_policy GoogleComputeBackendService#custom_policy}
        :param policy: policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#policy GoogleComputeBackendService#policy}
        '''
        if isinstance(custom_policy, dict):
            custom_policy = GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy(**custom_policy)
        if isinstance(policy, dict):
            policy = GoogleComputeBackendServiceLocalityLbPoliciesPolicy(**policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1710c9025436d7e4a0453b528d8d71e5b1e18a792c93179b8fec8f47d468c0d)
            check_type(argname="argument custom_policy", value=custom_policy, expected_type=type_hints["custom_policy"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_policy is not None:
            self._values["custom_policy"] = custom_policy
        if policy is not None:
            self._values["policy"] = policy

    @builtins.property
    def custom_policy(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy"]:
        '''custom_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#custom_policy GoogleComputeBackendService#custom_policy}
        '''
        result = self._values.get("custom_policy")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy"], result)

    @builtins.property
    def policy(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceLocalityLbPoliciesPolicy"]:
        '''policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#policy GoogleComputeBackendService#policy}
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceLocalityLbPoliciesPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceLocalityLbPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "data": "data"},
)
class GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy:
    def __init__(
        self,
        *,
        name: builtins.str,
        data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Identifies the custom policy. The value should match the type the custom implementation is registered with on the gRPC clients. It should follow protocol buffer message naming conventions and include the full path (e.g. myorg.CustomLbPolicy). The maximum length is 256 characters. Note that specifying the same custom policy more than once for a backend is not a valid configuration and will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        :param data: An optional, arbitrary JSON object with configuration data, understood by a locally installed custom policy implementation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#data GoogleComputeBackendService#data}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ade4ddfae6a739c4d6776c5a4dbe2910dbf87d6b3ece8b2fb63cd13269a59f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if data is not None:
            self._values["data"] = data

    @builtins.property
    def name(self) -> builtins.str:
        '''Identifies the custom policy.

        The value should match the type the custom implementation is registered
        with on the gRPC clients. It should follow protocol buffer
        message naming conventions and include the full path (e.g.
        myorg.CustomLbPolicy). The maximum length is 256 characters.

        Note that specifying the same custom policy more than once for a
        backend is not a valid configuration and will be rejected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''An optional, arbitrary JSON object with configuration data, understood by a locally installed custom policy implementation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#data GoogleComputeBackendService#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__778c1abccf536e7718052866e860867a2c78fb9f39372e922be161918f06c7e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "data"))

    @data.setter
    def data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f66b37f7bddf91facb74431847d672f5fa5134578345fd24d0e7aad1376e1d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65264707631adc0f19af9be6fc3afb11459d06ca970fd766dcb273d6c2f85251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac9d8d2bd655a8217d676a840d185c5cd2d255b60e739c8f5f1aa701c67f97b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeBackendServiceLocalityLbPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceLocalityLbPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__285908e2b5af5b4cfa283d3e45df31db15911ba650dd07f59b012be7af92590c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeBackendServiceLocalityLbPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ffcc130faca41dc2782112455a2e0b23981587a37d2d7d71c846b9812f6f91)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeBackendServiceLocalityLbPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a8cc4ae0d3f0c2001351af1b8d09868254fa477180c2518d23e6da01d00fff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4b32769f50e7d08e83eccf5bfe0592a6a820db32ef3946ae06c353cb70178a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4feb3e64b3fb3d35a246187c175f3de71a7141dbee32fe0eefdd9e0dba951026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceLocalityLbPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceLocalityLbPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceLocalityLbPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db9aa468ab9c4f718abf96386a9085bd22b299158eb3257179c9d51b29d6788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeBackendServiceLocalityLbPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceLocalityLbPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cc5ec9ee35180e228ad623b9bac64d619d0d056c20b25cd3c15ff13f5f3fbb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomPolicy")
    def put_custom_policy(
        self,
        *,
        name: builtins.str,
        data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Identifies the custom policy. The value should match the type the custom implementation is registered with on the gRPC clients. It should follow protocol buffer message naming conventions and include the full path (e.g. myorg.CustomLbPolicy). The maximum length is 256 characters. Note that specifying the same custom policy more than once for a backend is not a valid configuration and will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        :param data: An optional, arbitrary JSON object with configuration data, understood by a locally installed custom policy implementation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#data GoogleComputeBackendService#data}
        '''
        value = GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy(
            name=name, data=data
        )

        return typing.cast(None, jsii.invoke(self, "putCustomPolicy", [value]))

    @jsii.member(jsii_name="putPolicy")
    def put_policy(self, *, name: builtins.str) -> None:
        '''
        :param name: The name of a locality load balancer policy to be used. The value should be one of the predefined ones as supported by localityLbPolicy, although at the moment only ROUND_ROBIN is supported. This field should only be populated when the customPolicy field is not used. Note that specifying the same policy more than once for a backend is not a valid configuration and will be rejected. The possible values are: - 'ROUND_ROBIN': This is a simple policy in which each healthy backend is selected in round robin order. - 'LEAST_REQUEST': An O(1) algorithm which selects two random healthy hosts and picks the host which has fewer active requests. - 'RING_HASH': The ring/modulo hash load balancer implements consistent hashing to backends. The algorithm has the property that the addition/removal of a host from a set of N hosts only affects 1/N of the requests. - 'RANDOM': The load balancer selects a random healthy host. - 'ORIGINAL_DESTINATION': Backend host is selected based on the client connection metadata, i.e., connections are opened to the same address as the destination address of the incoming connection before the connection was redirected to the load balancer. - 'MAGLEV': used as a drop in replacement for the ring hash load balancer. Maglev is not as stable as ring hash but has faster table lookup build times and host selection times. For more information about Maglev, refer to https://ai.google/research/pubs/pub44824 Possible values: ["ROUND_ROBIN", "LEAST_REQUEST", "RING_HASH", "RANDOM", "ORIGINAL_DESTINATION", "MAGLEV"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        '''
        value = GoogleComputeBackendServiceLocalityLbPoliciesPolicy(name=name)

        return typing.cast(None, jsii.invoke(self, "putPolicy", [value]))

    @jsii.member(jsii_name="resetCustomPolicy")
    def reset_custom_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomPolicy", []))

    @jsii.member(jsii_name="resetPolicy")
    def reset_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="customPolicy")
    def custom_policy(
        self,
    ) -> GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicyOutputReference:
        return typing.cast(GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicyOutputReference, jsii.get(self, "customPolicy"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(
        self,
    ) -> "GoogleComputeBackendServiceLocalityLbPoliciesPolicyOutputReference":
        return typing.cast("GoogleComputeBackendServiceLocalityLbPoliciesPolicyOutputReference", jsii.get(self, "policy"))

    @builtins.property
    @jsii.member(jsii_name="customPolicyInput")
    def custom_policy_input(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy], jsii.get(self, "customPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceLocalityLbPoliciesPolicy"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceLocalityLbPoliciesPolicy"], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceLocalityLbPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceLocalityLbPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceLocalityLbPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4356f9c934c17dee85d42a6bd9de981a7056a4f76e0580c5c34bce9fb6e67cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceLocalityLbPoliciesPolicy",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleComputeBackendServiceLocalityLbPoliciesPolicy:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: The name of a locality load balancer policy to be used. The value should be one of the predefined ones as supported by localityLbPolicy, although at the moment only ROUND_ROBIN is supported. This field should only be populated when the customPolicy field is not used. Note that specifying the same policy more than once for a backend is not a valid configuration and will be rejected. The possible values are: - 'ROUND_ROBIN': This is a simple policy in which each healthy backend is selected in round robin order. - 'LEAST_REQUEST': An O(1) algorithm which selects two random healthy hosts and picks the host which has fewer active requests. - 'RING_HASH': The ring/modulo hash load balancer implements consistent hashing to backends. The algorithm has the property that the addition/removal of a host from a set of N hosts only affects 1/N of the requests. - 'RANDOM': The load balancer selects a random healthy host. - 'ORIGINAL_DESTINATION': Backend host is selected based on the client connection metadata, i.e., connections are opened to the same address as the destination address of the incoming connection before the connection was redirected to the load balancer. - 'MAGLEV': used as a drop in replacement for the ring hash load balancer. Maglev is not as stable as ring hash but has faster table lookup build times and host selection times. For more information about Maglev, refer to https://ai.google/research/pubs/pub44824 Possible values: ["ROUND_ROBIN", "LEAST_REQUEST", "RING_HASH", "RANDOM", "ORIGINAL_DESTINATION", "MAGLEV"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d7e43e9ee9ecb81bde5c888d550a2140e75e5d4623bf44426aeec41386d9ee)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of a locality load balancer policy to be used.

        The value
        should be one of the predefined ones as supported by localityLbPolicy,
        although at the moment only ROUND_ROBIN is supported.

        This field should only be populated when the customPolicy field is not
        used.

        Note that specifying the same policy more than once for a backend is
        not a valid configuration and will be rejected.

        The possible values are:

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
          Maglev, refer to https://ai.google/research/pubs/pub44824 Possible values: ["ROUND_ROBIN", "LEAST_REQUEST", "RING_HASH", "RANDOM", "ORIGINAL_DESTINATION", "MAGLEV"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceLocalityLbPoliciesPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceLocalityLbPoliciesPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceLocalityLbPoliciesPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b039a9739e928696a172ab45beda86747bf7f2ef43beaedfc490d2fd559ccefa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__06b1ea765139040773036eaf93caebe771dc5e64d6ddf3684a28def3eae2e3d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceLocalityLbPoliciesPolicy]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceLocalityLbPoliciesPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceLocalityLbPoliciesPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb877d742a764a7053174625d039cd4c2253f5eff57f954a9d8572e7a956f837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceLogConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable": "enable",
        "optional_fields": "optionalFields",
        "optional_mode": "optionalMode",
        "sample_rate": "sampleRate",
    },
)
class GoogleComputeBackendServiceLogConfig:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        optional_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        optional_mode: typing.Optional[builtins.str] = None,
        sample_rate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enable: Whether to enable logging for the load balancer traffic served by this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enable GoogleComputeBackendService#enable}
        :param optional_fields: This field can only be specified if logging is enabled for this backend service and "logConfig.optionalMode" was set to CUSTOM. Contains a list of optional fields you want to include in the logs. For example: serverInstance, serverGkeDetails.cluster, serverGkeDetails.pod.podNamespace For example: orca_load_report, tls.protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#optional_fields GoogleComputeBackendService#optional_fields}
        :param optional_mode: Specifies the optional logging mode for the load balancer traffic. Supported values: INCLUDE_ALL_OPTIONAL, EXCLUDE_ALL_OPTIONAL, CUSTOM. Possible values: ["INCLUDE_ALL_OPTIONAL", "EXCLUDE_ALL_OPTIONAL", "CUSTOM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#optional_mode GoogleComputeBackendService#optional_mode}
        :param sample_rate: This field can only be specified if logging is enabled for this backend service. The value of the field must be in [0, 1]. This configures the sampling rate of requests to the load balancer where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported. The default value is 1.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#sample_rate GoogleComputeBackendService#sample_rate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0de60b5260e5df51352f3d144e6ecc0ffa44de01a5ae46e68a73835bc34cb5f1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enable GoogleComputeBackendService#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def optional_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''This field can only be specified if logging is enabled for this backend service and "logConfig.optionalMode" was set to CUSTOM. Contains a list of optional fields you want to include in the logs. For example: serverInstance, serverGkeDetails.cluster, serverGkeDetails.pod.podNamespace For example: orca_load_report, tls.protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#optional_fields GoogleComputeBackendService#optional_fields}
        '''
        result = self._values.get("optional_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def optional_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the optional logging mode for the load balancer traffic. Supported values: INCLUDE_ALL_OPTIONAL, EXCLUDE_ALL_OPTIONAL, CUSTOM. Possible values: ["INCLUDE_ALL_OPTIONAL", "EXCLUDE_ALL_OPTIONAL", "CUSTOM"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#optional_mode GoogleComputeBackendService#optional_mode}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#sample_rate GoogleComputeBackendService#sample_rate}
        '''
        result = self._values.get("sample_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4208278a042a889d2a2edc354b4aad9db523e97da04d3d0278477dea81a4260)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7722e4377a319d4965eff31e5d53b925f7df0859605b70dad823875e4eb236dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optionalFields")
    def optional_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "optionalFields"))

    @optional_fields.setter
    def optional_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00465a0936cbed90659fbfa45f0b4457f71628f745d121ede59ffe80d36089e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionalFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optionalMode")
    def optional_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "optionalMode"))

    @optional_mode.setter
    def optional_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f490b272039c35b3e5c8cf5bf0b0b3b1ca4190c3a66e53d8f2dae65fff0b4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionalMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleRate")
    def sample_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleRate"))

    @sample_rate.setter
    def sample_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9d529cc4bbf82008e3add44c5bf42b4149c72bb05979566201c23a3cec1306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComputeBackendServiceLogConfig]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90d33f5e2d4509e50387e91e1e1bfbe6316f3d05146afb92317e759ccd8e2e4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceMaxStreamDuration",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class GoogleComputeBackendServiceMaxStreamDuration:
    def __init__(
        self,
        *,
        seconds: builtins.str,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. (int64 format). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e881db160ff172eaa692d5743b2a5f6a451e13866172ffc6237d3e2512a601a)
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "seconds": seconds,
        }
        if nanos is not None:
            self._values["nanos"] = nanos

    @builtins.property
    def seconds(self) -> builtins.str:
        '''Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. (int64 format).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
        '''
        result = self._values.get("seconds")
        assert result is not None, "Required property 'seconds' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Span of time that's a fraction of a second at nanosecond resolution.

        Durations less than one second are represented with a 0 seconds field and a positive nanos field.
        Must be from 0 to 999,999,999 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceMaxStreamDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceMaxStreamDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceMaxStreamDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a16d109b2489da771d3b2a76bc7f661681f78372a061d4ae11854b35dd91c0af)
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
    def seconds_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09d94670ec1d52cf76eb3cc701126d7d8dfd7fc47142a2272835f7a141bf899a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4b54621a2f2b0f484467d2dd5894c3d298a38ffe2c7b62237bed37c29f89a16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceMaxStreamDuration]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceMaxStreamDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceMaxStreamDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__770f8fe692256769e0908712b2836e59ceb53f38b0d44c2b88006e7ff3e84707)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy",
    jsii_struct_bases=[],
    name_mapping={"zonal_affinity": "zonalAffinity"},
)
class GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy:
    def __init__(
        self,
        *,
        zonal_affinity: typing.Optional[typing.Union["GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param zonal_affinity: zonal_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#zonal_affinity GoogleComputeBackendService#zonal_affinity}
        '''
        if isinstance(zonal_affinity, dict):
            zonal_affinity = GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity(**zonal_affinity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14206293ac19beb44adb022233c0d77a43a8348745f82aaceb574ce2a5c6caae)
            check_type(argname="argument zonal_affinity", value=zonal_affinity, expected_type=type_hints["zonal_affinity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if zonal_affinity is not None:
            self._values["zonal_affinity"] = zonal_affinity

    @builtins.property
    def zonal_affinity(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity"]:
        '''zonal_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#zonal_affinity GoogleComputeBackendService#zonal_affinity}
        '''
        result = self._values.get("zonal_affinity")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cf74043f85cce4fa359dca4a60cddbdb6a2682c95cd82f265cb3fee7dab8ffc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putZonalAffinity")
    def put_zonal_affinity(
        self,
        *,
        spillover: typing.Optional[builtins.str] = None,
        spillover_ratio: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param spillover: This field indicates whether zonal affinity is enabled or not. Default value: "ZONAL_AFFINITY_DISABLED" Possible values: ["ZONAL_AFFINITY_DISABLED", "ZONAL_AFFINITY_SPILL_CROSS_ZONE", "ZONAL_AFFINITY_STAY_WITHIN_ZONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#spillover GoogleComputeBackendService#spillover}
        :param spillover_ratio: The value of the field must be in [0, 1]. When the ratio of the count of healthy backend endpoints in a zone to the count of backend endpoints in that same zone is equal to or above this threshold, the load balancer distributes new connections to all healthy endpoints in the local zone only. When the ratio of the count of healthy backend endpoints in a zone to the count of backend endpoints in that same zone is below this threshold, the load balancer distributes all new connections to all healthy endpoints across all zones. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#spillover_ratio GoogleComputeBackendService#spillover_ratio}
        '''
        value = GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity(
            spillover=spillover, spillover_ratio=spillover_ratio
        )

        return typing.cast(None, jsii.invoke(self, "putZonalAffinity", [value]))

    @jsii.member(jsii_name="resetZonalAffinity")
    def reset_zonal_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZonalAffinity", []))

    @builtins.property
    @jsii.member(jsii_name="zonalAffinity")
    def zonal_affinity(
        self,
    ) -> "GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinityOutputReference":
        return typing.cast("GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinityOutputReference", jsii.get(self, "zonalAffinity"))

    @builtins.property
    @jsii.member(jsii_name="zonalAffinityInput")
    def zonal_affinity_input(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity"], jsii.get(self, "zonalAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d2055fb7131780380a8228f0724bb00fd54db3d2a318d76b2220587700e5d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity",
    jsii_struct_bases=[],
    name_mapping={"spillover": "spillover", "spillover_ratio": "spilloverRatio"},
)
class GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity:
    def __init__(
        self,
        *,
        spillover: typing.Optional[builtins.str] = None,
        spillover_ratio: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param spillover: This field indicates whether zonal affinity is enabled or not. Default value: "ZONAL_AFFINITY_DISABLED" Possible values: ["ZONAL_AFFINITY_DISABLED", "ZONAL_AFFINITY_SPILL_CROSS_ZONE", "ZONAL_AFFINITY_STAY_WITHIN_ZONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#spillover GoogleComputeBackendService#spillover}
        :param spillover_ratio: The value of the field must be in [0, 1]. When the ratio of the count of healthy backend endpoints in a zone to the count of backend endpoints in that same zone is equal to or above this threshold, the load balancer distributes new connections to all healthy endpoints in the local zone only. When the ratio of the count of healthy backend endpoints in a zone to the count of backend endpoints in that same zone is below this threshold, the load balancer distributes all new connections to all healthy endpoints across all zones. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#spillover_ratio GoogleComputeBackendService#spillover_ratio}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59d7b901af8f06b4ad0c2e0f0230350ec91fdcb54926da862a918e2af808681b)
            check_type(argname="argument spillover", value=spillover, expected_type=type_hints["spillover"])
            check_type(argname="argument spillover_ratio", value=spillover_ratio, expected_type=type_hints["spillover_ratio"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if spillover is not None:
            self._values["spillover"] = spillover
        if spillover_ratio is not None:
            self._values["spillover_ratio"] = spillover_ratio

    @builtins.property
    def spillover(self) -> typing.Optional[builtins.str]:
        '''This field indicates whether zonal affinity is enabled or not. Default value: "ZONAL_AFFINITY_DISABLED" Possible values: ["ZONAL_AFFINITY_DISABLED", "ZONAL_AFFINITY_SPILL_CROSS_ZONE", "ZONAL_AFFINITY_STAY_WITHIN_ZONE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#spillover GoogleComputeBackendService#spillover}
        '''
        result = self._values.get("spillover")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spillover_ratio(self) -> typing.Optional[jsii.Number]:
        '''The value of the field must be in [0, 1].

        When the ratio of the count of healthy backend endpoints in a zone
        to the count of backend endpoints in that same zone is equal to or above this threshold, the load balancer
        distributes new connections to all healthy endpoints in the local zone only. When the ratio of the count
        of healthy backend endpoints in a zone to the count of backend endpoints in that same zone is below this
        threshold, the load balancer distributes all new connections to all healthy endpoints across all zones.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#spillover_ratio GoogleComputeBackendService#spillover_ratio}
        '''
        result = self._values.get("spillover_ratio")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9785c09b898c4270814c41f86420506ab95bcd60ea46234594c68c76d7042cd6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSpillover")
    def reset_spillover(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpillover", []))

    @jsii.member(jsii_name="resetSpilloverRatio")
    def reset_spillover_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpilloverRatio", []))

    @builtins.property
    @jsii.member(jsii_name="spilloverInput")
    def spillover_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spilloverInput"))

    @builtins.property
    @jsii.member(jsii_name="spilloverRatioInput")
    def spillover_ratio_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "spilloverRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="spillover")
    def spillover(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spillover"))

    @spillover.setter
    def spillover(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa8b365f4e4876e35f464ebd546eb5511b8258836b726616a9b29775aa260d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spillover", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spilloverRatio")
    def spillover_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "spilloverRatio"))

    @spillover_ratio.setter
    def spillover_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc0cd707c97432df0fbf893fc04c4e6a43ea8cf600397a2bde2d6e7f6156807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spilloverRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2200260f0e712c48da7708358a8ecdb25460fadd68a5e22a1de86dc1327ce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceOutlierDetection",
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
class GoogleComputeBackendServiceOutlierDetection:
    def __init__(
        self,
        *,
        base_ejection_time: typing.Optional[typing.Union["GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime", typing.Dict[builtins.str, typing.Any]]] = None,
        consecutive_errors: typing.Optional[jsii.Number] = None,
        consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_errors: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_success_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[typing.Union["GoogleComputeBackendServiceOutlierDetectionInterval", typing.Dict[builtins.str, typing.Any]]] = None,
        max_ejection_percent: typing.Optional[jsii.Number] = None,
        success_rate_minimum_hosts: typing.Optional[jsii.Number] = None,
        success_rate_request_volume: typing.Optional[jsii.Number] = None,
        success_rate_stdev_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param base_ejection_time: base_ejection_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#base_ejection_time GoogleComputeBackendService#base_ejection_time}
        :param consecutive_errors: Number of errors before a host is ejected from the connection pool. When the backend host is accessed over HTTP, a 5xx return code qualifies as an error. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#consecutive_errors GoogleComputeBackendService#consecutive_errors}
        :param consecutive_gateway_failure: The number of consecutive gateway failures (502, 503, 504 status or connection errors that are mapped to one of those status codes) before a consecutive gateway failure ejection occurs. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#consecutive_gateway_failure GoogleComputeBackendService#consecutive_gateway_failure}
        :param enforcing_consecutive_errors: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive 5xx. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enforcing_consecutive_errors GoogleComputeBackendService#enforcing_consecutive_errors}
        :param enforcing_consecutive_gateway_failure: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive gateway failures. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enforcing_consecutive_gateway_failure GoogleComputeBackendService#enforcing_consecutive_gateway_failure}
        :param enforcing_success_rate: The percentage chance that a host will be actually ejected when an outlier status is detected through success rate statistics. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enforcing_success_rate GoogleComputeBackendService#enforcing_success_rate}
        :param interval: interval block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#interval GoogleComputeBackendService#interval}
        :param max_ejection_percent: Maximum percentage of hosts in the load balancing pool for the backend service that can be ejected. Defaults to 10%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_ejection_percent GoogleComputeBackendService#max_ejection_percent}
        :param success_rate_minimum_hosts: The number of hosts in a cluster that must have enough request volume to detect success rate outliers. If the number of hosts is less than this setting, outlier detection via success rate statistics is not performed for any host in the cluster. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#success_rate_minimum_hosts GoogleComputeBackendService#success_rate_minimum_hosts}
        :param success_rate_request_volume: The minimum number of total requests that must be collected in one interval (as defined by the interval duration above) to include this host in success rate based outlier detection. If the volume is lower than this setting, outlier detection via success rate statistics is not performed for that host. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#success_rate_request_volume GoogleComputeBackendService#success_rate_request_volume}
        :param success_rate_stdev_factor: This factor is used to determine the ejection threshold for success rate outlier ejection. The ejection threshold is the difference between the mean success rate, and the product of this factor and the standard deviation of the mean success rate: mean - (stdev * success_rate_stdev_factor). This factor is divided by a thousand to get a double. That is, if the desired factor is 1.9, the runtime value should be 1900. Defaults to 1900. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#success_rate_stdev_factor GoogleComputeBackendService#success_rate_stdev_factor}
        '''
        if isinstance(base_ejection_time, dict):
            base_ejection_time = GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime(**base_ejection_time)
        if isinstance(interval, dict):
            interval = GoogleComputeBackendServiceOutlierDetectionInterval(**interval)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f8936a47f2241d620b0584e8298e9238c034306cbf08e400e9c89e7fcf85a3)
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
    ) -> typing.Optional["GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime"]:
        '''base_ejection_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#base_ejection_time GoogleComputeBackendService#base_ejection_time}
        '''
        result = self._values.get("base_ejection_time")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime"], result)

    @builtins.property
    def consecutive_errors(self) -> typing.Optional[jsii.Number]:
        '''Number of errors before a host is ejected from the connection pool.

        When the
        backend host is accessed over HTTP, a 5xx return code qualifies as an error.
        Defaults to 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#consecutive_errors GoogleComputeBackendService#consecutive_errors}
        '''
        result = self._values.get("consecutive_errors")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def consecutive_gateway_failure(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive gateway failures (502, 503, 504 status or connection errors that are mapped to one of those status codes) before a consecutive gateway failure ejection occurs.

        Defaults to 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#consecutive_gateway_failure GoogleComputeBackendService#consecutive_gateway_failure}
        '''
        result = self._values.get("consecutive_gateway_failure")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enforcing_consecutive_errors(self) -> typing.Optional[jsii.Number]:
        '''The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive 5xx.

        This setting can be used to disable
        ejection or to ramp it up slowly. Defaults to 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enforcing_consecutive_errors GoogleComputeBackendService#enforcing_consecutive_errors}
        '''
        result = self._values.get("enforcing_consecutive_errors")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enforcing_consecutive_gateway_failure(self) -> typing.Optional[jsii.Number]:
        '''The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive gateway failures.

        This setting can be
        used to disable ejection or to ramp it up slowly. Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enforcing_consecutive_gateway_failure GoogleComputeBackendService#enforcing_consecutive_gateway_failure}
        '''
        result = self._values.get("enforcing_consecutive_gateway_failure")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enforcing_success_rate(self) -> typing.Optional[jsii.Number]:
        '''The percentage chance that a host will be actually ejected when an outlier status is detected through success rate statistics.

        This setting can be used to
        disable ejection or to ramp it up slowly. Defaults to 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#enforcing_success_rate GoogleComputeBackendService#enforcing_success_rate}
        '''
        result = self._values.get("enforcing_success_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceOutlierDetectionInterval"]:
        '''interval block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#interval GoogleComputeBackendService#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceOutlierDetectionInterval"], result)

    @builtins.property
    def max_ejection_percent(self) -> typing.Optional[jsii.Number]:
        '''Maximum percentage of hosts in the load balancing pool for the backend service that can be ejected. Defaults to 10%.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#max_ejection_percent GoogleComputeBackendService#max_ejection_percent}
        '''
        result = self._values.get("max_ejection_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_rate_minimum_hosts(self) -> typing.Optional[jsii.Number]:
        '''The number of hosts in a cluster that must have enough request volume to detect success rate outliers.

        If the number of hosts is less than this setting, outlier
        detection via success rate statistics is not performed for any host in the
        cluster. Defaults to 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#success_rate_minimum_hosts GoogleComputeBackendService#success_rate_minimum_hosts}
        '''
        result = self._values.get("success_rate_minimum_hosts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_rate_request_volume(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of total requests that must be collected in one interval (as defined by the interval duration above) to include this host in success rate based outlier detection.

        If the volume is lower than this setting, outlier
        detection via success rate statistics is not performed for that host. Defaults
        to 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#success_rate_request_volume GoogleComputeBackendService#success_rate_request_volume}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#success_rate_stdev_factor GoogleComputeBackendService#success_rate_stdev_factor}
        '''
        result = self._values.get("success_rate_stdev_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceOutlierDetection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9709c4013f0d03f53d30f4ca0ab1e74adf7f058a3eb94d2169db29d146d99b2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceOutlierDetectionBaseEjectionTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceOutlierDetectionBaseEjectionTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c88d60875d56dcf455a4e040b9bf4babf9fdbf913ea875f039c81b14261bc09b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__792f01fd4d4c581cf7e95e78cb671e2a5499f823421583f4eebb2e819b6a9dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e91579c97d1bead8489be5b921cdad4a3687e2c5e2f5262aa7173915267daa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe0f0affd12e028a305475a77c71756b2b4079f2454f2517c536d8bec660d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceOutlierDetectionInterval",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class GoogleComputeBackendServiceOutlierDetectionInterval:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a6701307ce40baffd213c3dee0e59f56bf604db9b680fba438ee80c05917ed4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceOutlierDetectionInterval(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceOutlierDetectionIntervalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceOutlierDetectionIntervalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33e8f0dca10d471e38fb5ad2a5373a6ec54dd0edce88fea129e62d1007d0fcef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80731407ace21a8a501138ad4aaafb43e5605d8e1e31c20b03e741869783d329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a917cef0c3e11a13047741d244a69a845880cd973e8a984d1ddb7a5126a135da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceOutlierDetectionInterval]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceOutlierDetectionInterval], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceOutlierDetectionInterval],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__058b05c60dd1cc6fc99cfcfdcef7ec3904ff5e68e6f84aab60b080779f03720a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeBackendServiceOutlierDetectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceOutlierDetectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6884998680063082d1d313ac65b8c62c3ae9db98973823c19d68c372862e956)
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        value = GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime(
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        value = GoogleComputeBackendServiceOutlierDetectionInterval(
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
    ) -> GoogleComputeBackendServiceOutlierDetectionBaseEjectionTimeOutputReference:
        return typing.cast(GoogleComputeBackendServiceOutlierDetectionBaseEjectionTimeOutputReference, jsii.get(self, "baseEjectionTime"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(
        self,
    ) -> GoogleComputeBackendServiceOutlierDetectionIntervalOutputReference:
        return typing.cast(GoogleComputeBackendServiceOutlierDetectionIntervalOutputReference, jsii.get(self, "interval"))

    @builtins.property
    @jsii.member(jsii_name="baseEjectionTimeInput")
    def base_ejection_time_input(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime], jsii.get(self, "baseEjectionTimeInput"))

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
    ) -> typing.Optional[GoogleComputeBackendServiceOutlierDetectionInterval]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceOutlierDetectionInterval], jsii.get(self, "intervalInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__42ef50129945c3789c215506d579cedd3b52d0c549e900d53e7d99dfc2284f35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consecutiveErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consecutiveGatewayFailure")
    def consecutive_gateway_failure(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "consecutiveGatewayFailure"))

    @consecutive_gateway_failure.setter
    def consecutive_gateway_failure(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88ac30c4abb564c7a7d9c458f1a24fa77c67a6db572d9b75f661bebd007c37f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consecutiveGatewayFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcingConsecutiveErrors")
    def enforcing_consecutive_errors(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "enforcingConsecutiveErrors"))

    @enforcing_consecutive_errors.setter
    def enforcing_consecutive_errors(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56678f1c607581870529f669e2827a1f4533b67b13b7bf7b83a94007de7265ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcingConsecutiveErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcingConsecutiveGatewayFailure")
    def enforcing_consecutive_gateway_failure(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "enforcingConsecutiveGatewayFailure"))

    @enforcing_consecutive_gateway_failure.setter
    def enforcing_consecutive_gateway_failure(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d357fe5dd19f518b63f14bdc51cfcbe084ce9221eeb1aeac9b1aa17c00c498d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcingConsecutiveGatewayFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcingSuccessRate")
    def enforcing_success_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "enforcingSuccessRate"))

    @enforcing_success_rate.setter
    def enforcing_success_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dabc43947cfb61a2580f3c480d99b40d681eed0d83167414ce61b7b676232ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcingSuccessRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxEjectionPercent")
    def max_ejection_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxEjectionPercent"))

    @max_ejection_percent.setter
    def max_ejection_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb814e298e54c32ce76c5a7f9e54d3e25039b5ded260ce88bd9fb7b5b85d25e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxEjectionPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successRateMinimumHosts")
    def success_rate_minimum_hosts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successRateMinimumHosts"))

    @success_rate_minimum_hosts.setter
    def success_rate_minimum_hosts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b96ba5951aae43be63b5239a13604d0c2267a7dc1b5ee442f5bd683f0ae932fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successRateMinimumHosts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successRateRequestVolume")
    def success_rate_request_volume(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successRateRequestVolume"))

    @success_rate_request_volume.setter
    def success_rate_request_volume(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ac486e53c92c77df7cba602548c549eac8939cd32d117418f5b19352f3ec76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successRateRequestVolume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successRateStdevFactor")
    def success_rate_stdev_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successRateStdevFactor"))

    @success_rate_stdev_factor.setter
    def success_rate_stdev_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb25ec655890cdb2019a250f03a4c0924801cb75d82ed54a5b59cc1ad86ee1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successRateStdevFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceOutlierDetection]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceOutlierDetection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceOutlierDetection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03f98e32708a1da291fe16e3a4117d4df9cd7fcf170cd067a0e0629374e2970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceSecuritySettings",
    jsii_struct_bases=[],
    name_mapping={
        "aws_v4_authentication": "awsV4Authentication",
        "client_tls_policy": "clientTlsPolicy",
        "subject_alt_names": "subjectAltNames",
    },
)
class GoogleComputeBackendServiceSecuritySettings:
    def __init__(
        self,
        *,
        aws_v4_authentication: typing.Optional[typing.Union["GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication", typing.Dict[builtins.str, typing.Any]]] = None,
        client_tls_policy: typing.Optional[builtins.str] = None,
        subject_alt_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param aws_v4_authentication: aws_v4_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#aws_v4_authentication GoogleComputeBackendService#aws_v4_authentication}
        :param client_tls_policy: ClientTlsPolicy is a resource that specifies how a client should authenticate connections to backends of a service. This resource itself does not affect configuration unless it is attached to a backend service resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#client_tls_policy GoogleComputeBackendService#client_tls_policy}
        :param subject_alt_names: A list of alternate names to verify the subject identity in the certificate. If specified, the client will verify that the server certificate's subject alt name matches one of the specified values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#subject_alt_names GoogleComputeBackendService#subject_alt_names}
        '''
        if isinstance(aws_v4_authentication, dict):
            aws_v4_authentication = GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication(**aws_v4_authentication)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d3816b9701dd67e65619dfc27ce28114ba7ab18052ec960bd13eb59f99edfa1)
            check_type(argname="argument aws_v4_authentication", value=aws_v4_authentication, expected_type=type_hints["aws_v4_authentication"])
            check_type(argname="argument client_tls_policy", value=client_tls_policy, expected_type=type_hints["client_tls_policy"])
            check_type(argname="argument subject_alt_names", value=subject_alt_names, expected_type=type_hints["subject_alt_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_v4_authentication is not None:
            self._values["aws_v4_authentication"] = aws_v4_authentication
        if client_tls_policy is not None:
            self._values["client_tls_policy"] = client_tls_policy
        if subject_alt_names is not None:
            self._values["subject_alt_names"] = subject_alt_names

    @builtins.property
    def aws_v4_authentication(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication"]:
        '''aws_v4_authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#aws_v4_authentication GoogleComputeBackendService#aws_v4_authentication}
        '''
        result = self._values.get("aws_v4_authentication")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication"], result)

    @builtins.property
    def client_tls_policy(self) -> typing.Optional[builtins.str]:
        '''ClientTlsPolicy is a resource that specifies how a client should authenticate connections to backends of a service.

        This resource itself does not affect
        configuration unless it is attached to a backend service resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#client_tls_policy GoogleComputeBackendService#client_tls_policy}
        '''
        result = self._values.get("client_tls_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_alt_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of alternate names to verify the subject identity in the certificate.

        If specified, the client will verify that the server certificate's subject
        alt name matches one of the specified values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#subject_alt_names GoogleComputeBackendService#subject_alt_names}
        '''
        result = self._values.get("subject_alt_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceSecuritySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication",
    jsii_struct_bases=[],
    name_mapping={
        "access_key": "accessKey",
        "access_key_id": "accessKeyId",
        "access_key_version": "accessKeyVersion",
        "origin_region": "originRegion",
    },
)
class GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication:
    def __init__(
        self,
        *,
        access_key: typing.Optional[builtins.str] = None,
        access_key_id: typing.Optional[builtins.str] = None,
        access_key_version: typing.Optional[builtins.str] = None,
        origin_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_key: The access key used for s3 bucket authentication. Required for updating or creating a backend that uses AWS v4 signature authentication, but will not be returned as part of the configuration when queried with a REST API GET request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#access_key GoogleComputeBackendService#access_key}
        :param access_key_id: The identifier of an access key used for s3 bucket authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#access_key_id GoogleComputeBackendService#access_key_id}
        :param access_key_version: The optional version identifier for the access key. You can use this to keep track of different iterations of your access key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#access_key_version GoogleComputeBackendService#access_key_version}
        :param origin_region: The name of the cloud region of your origin. This is a free-form field with the name of the region your cloud uses to host your origin. For example, "us-east-1" for AWS or "us-ashburn-1" for OCI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#origin_region GoogleComputeBackendService#origin_region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9554c4214507ad54b18d225a7ce2131a461d04a30f03513c43f4702d6101e6)
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
            check_type(argname="argument access_key_version", value=access_key_version, expected_type=type_hints["access_key_version"])
            check_type(argname="argument origin_region", value=origin_region, expected_type=type_hints["origin_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_key is not None:
            self._values["access_key"] = access_key
        if access_key_id is not None:
            self._values["access_key_id"] = access_key_id
        if access_key_version is not None:
            self._values["access_key_version"] = access_key_version
        if origin_region is not None:
            self._values["origin_region"] = origin_region

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''The access key used for s3 bucket authentication.

        Required for updating or creating a backend that uses AWS v4 signature authentication, but will not be returned as part of the configuration when queried with a REST API GET request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#access_key GoogleComputeBackendService#access_key}
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of an access key used for s3 bucket authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#access_key_id GoogleComputeBackendService#access_key_id}
        '''
        result = self._values.get("access_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_key_version(self) -> typing.Optional[builtins.str]:
        '''The optional version identifier for the access key.

        You can use this to keep track of different iterations of your access key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#access_key_version GoogleComputeBackendService#access_key_version}
        '''
        result = self._values.get("access_key_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_region(self) -> typing.Optional[builtins.str]:
        '''The name of the cloud region of your origin.

        This is a free-form field with the name of the region your cloud uses to host your origin.
        For example, "us-east-1" for AWS or "us-ashburn-1" for OCI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#origin_region GoogleComputeBackendService#origin_region}
        '''
        result = self._values.get("origin_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceSecuritySettingsAwsV4AuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceSecuritySettingsAwsV4AuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10e2db87ccd39dce4c2e158c8a31bd39fae391a107f5380bb411a34b6eda44f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessKey")
    def reset_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKey", []))

    @jsii.member(jsii_name="resetAccessKeyId")
    def reset_access_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKeyId", []))

    @jsii.member(jsii_name="resetAccessKeyVersion")
    def reset_access_key_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKeyVersion", []))

    @jsii.member(jsii_name="resetOriginRegion")
    def reset_origin_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginRegion", []))

    @builtins.property
    @jsii.member(jsii_name="accessKeyIdInput")
    def access_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKeyInput")
    def access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKeyVersionInput")
    def access_key_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="originRegionInput")
    def origin_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKey"))

    @access_key.setter
    def access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56f6c248559c4091724b7bc22f7f0ae5fbbf1b82d3975e0ef31ffb1ccdca290d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKeyId"))

    @access_key_id.setter
    def access_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5289b5398d8f75949866d65214dde766d07c8b3ef5443dd39859391849b7c964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessKeyVersion")
    def access_key_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKeyVersion"))

    @access_key_version.setter
    def access_key_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76773eebb2db7da208717870a969c4c8485ff30120468e7ab1622f24da03f6d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeyVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originRegion")
    def origin_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originRegion"))

    @origin_region.setter
    def origin_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a229de67ab6b818c4bac662d31ac5066eed466cc5b1afd8187451d57a3e3b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047ee8c37d3009b2761b0011f5e5b40a9cf47cc3f05c2185119e6654f151827b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeBackendServiceSecuritySettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceSecuritySettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95a46777b22ae74d280e31514fa2a4101e55bc0a1a77566d63a50f66ae8a0e99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAwsV4Authentication")
    def put_aws_v4_authentication(
        self,
        *,
        access_key: typing.Optional[builtins.str] = None,
        access_key_id: typing.Optional[builtins.str] = None,
        access_key_version: typing.Optional[builtins.str] = None,
        origin_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_key: The access key used for s3 bucket authentication. Required for updating or creating a backend that uses AWS v4 signature authentication, but will not be returned as part of the configuration when queried with a REST API GET request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#access_key GoogleComputeBackendService#access_key}
        :param access_key_id: The identifier of an access key used for s3 bucket authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#access_key_id GoogleComputeBackendService#access_key_id}
        :param access_key_version: The optional version identifier for the access key. You can use this to keep track of different iterations of your access key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#access_key_version GoogleComputeBackendService#access_key_version}
        :param origin_region: The name of the cloud region of your origin. This is a free-form field with the name of the region your cloud uses to host your origin. For example, "us-east-1" for AWS or "us-ashburn-1" for OCI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#origin_region GoogleComputeBackendService#origin_region}
        '''
        value = GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication(
            access_key=access_key,
            access_key_id=access_key_id,
            access_key_version=access_key_version,
            origin_region=origin_region,
        )

        return typing.cast(None, jsii.invoke(self, "putAwsV4Authentication", [value]))

    @jsii.member(jsii_name="resetAwsV4Authentication")
    def reset_aws_v4_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsV4Authentication", []))

    @jsii.member(jsii_name="resetClientTlsPolicy")
    def reset_client_tls_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientTlsPolicy", []))

    @jsii.member(jsii_name="resetSubjectAltNames")
    def reset_subject_alt_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectAltNames", []))

    @builtins.property
    @jsii.member(jsii_name="awsV4Authentication")
    def aws_v4_authentication(
        self,
    ) -> GoogleComputeBackendServiceSecuritySettingsAwsV4AuthenticationOutputReference:
        return typing.cast(GoogleComputeBackendServiceSecuritySettingsAwsV4AuthenticationOutputReference, jsii.get(self, "awsV4Authentication"))

    @builtins.property
    @jsii.member(jsii_name="awsV4AuthenticationInput")
    def aws_v4_authentication_input(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication], jsii.get(self, "awsV4AuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="clientTlsPolicyInput")
    def client_tls_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientTlsPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectAltNamesInput")
    def subject_alt_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subjectAltNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientTlsPolicy")
    def client_tls_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientTlsPolicy"))

    @client_tls_policy.setter
    def client_tls_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc406aba1aa9fd422913a354556b8d00b652c9d5d784c3d992a40695e9d8a8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTlsPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectAltNames")
    def subject_alt_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subjectAltNames"))

    @subject_alt_names.setter
    def subject_alt_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a351bc9198d2d66c12cb6b388e9afd52366edecc2f3834c925e01a5d0d365a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectAltNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceSecuritySettings]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceSecuritySettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceSecuritySettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7604f7a33ee86ccc1f766a5fc730ea621897b446a3e40f3285a3354e9e929528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceStrongSessionAffinityCookie",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "ttl": "ttl"},
)
class GoogleComputeBackendServiceStrongSessionAffinityCookie:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[typing.Union["GoogleComputeBackendServiceStrongSessionAffinityCookieTtl", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#path GoogleComputeBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#ttl GoogleComputeBackendService#ttl}
        '''
        if isinstance(ttl, dict):
            ttl = GoogleComputeBackendServiceStrongSessionAffinityCookieTtl(**ttl)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e042d74ead8dd73cdadb9339b61bae63ef850cd6dd1f868605fb315a86452a3d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#name GoogleComputeBackendService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to set for the cookie.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#path GoogleComputeBackendService#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(
        self,
    ) -> typing.Optional["GoogleComputeBackendServiceStrongSessionAffinityCookieTtl"]:
        '''ttl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#ttl GoogleComputeBackendService#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional["GoogleComputeBackendServiceStrongSessionAffinityCookieTtl"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceStrongSessionAffinityCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceStrongSessionAffinityCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceStrongSessionAffinityCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0a65dbc6a917207f69b79d6e104e77a10017b054d3c33e0f927b979f7226480)
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        value = GoogleComputeBackendServiceStrongSessionAffinityCookieTtl(
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
    ) -> "GoogleComputeBackendServiceStrongSessionAffinityCookieTtlOutputReference":
        return typing.cast("GoogleComputeBackendServiceStrongSessionAffinityCookieTtlOutputReference", jsii.get(self, "ttl"))

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
    ) -> typing.Optional["GoogleComputeBackendServiceStrongSessionAffinityCookieTtl"]:
        return typing.cast(typing.Optional["GoogleComputeBackendServiceStrongSessionAffinityCookieTtl"], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed87dfcae835ec6734ee477bcbd6c2a3a492736802937adc0c9445f5501c606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de364a6bc0677439b86b18acde300361ab69ba886359f4b710dc952508af7006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceStrongSessionAffinityCookie]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceStrongSessionAffinityCookie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceStrongSessionAffinityCookie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9e833cbd831e3b637541e13461da6597987fe9ad2a4a214d412c2f3afb4aa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceStrongSessionAffinityCookieTtl",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class GoogleComputeBackendServiceStrongSessionAffinityCookieTtl:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a4e718d66eb6c8302aeb36c32a232cb644219c96f6945e51fad10af5c5e0ff4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#seconds GoogleComputeBackendService#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#nanos GoogleComputeBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceStrongSessionAffinityCookieTtl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceStrongSessionAffinityCookieTtlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceStrongSessionAffinityCookieTtlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__144a1cf5595fb0d15b91a054b0f43bd53f7e041c4a15f51ef13c1530bc6e2070)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1dcb2eb5761f9466ce4a2d7820e3261e7bc95cdf8e6ed3dccf9b01ca173d0c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efea24fdd118f7dc96e3716170da5413a5f6c5f38f44b2094c997940faa5b735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeBackendServiceStrongSessionAffinityCookieTtl]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceStrongSessionAffinityCookieTtl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceStrongSessionAffinityCookieTtl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d83537f59e0e46014925624834a2e8d19da92a5e391caeaeb7aca98678e1ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeBackendServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#create GoogleComputeBackendService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#delete GoogleComputeBackendService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#update GoogleComputeBackendService#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b18ff9c68be1dd890a71586f233ee937fc72983ce6b151a8af7508460e92d29)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#create GoogleComputeBackendService#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#delete GoogleComputeBackendService#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#update GoogleComputeBackendService#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea63cd71c88d702fe945c899f0dddefda97064d9d9076098f362f00fe2cf5ddf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdb5137507cfb605d75429d5173ecaae56ddeaceecdc91f448090af43fb7e224)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3736db3d16224483cabe479b0a0b5ac0701fda430fda59872762fd92cb6de6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d647baad2099f7c57d65a33f008ef8c49f592ca55d8ef444de372ea7704830d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__744972ef4963ac7da436a151482f6a8bbe9038c8db20cf2a6b9842c7c09befca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceTlsSettings",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_config": "authenticationConfig",
        "sni": "sni",
        "subject_alt_names": "subjectAltNames",
    },
)
class GoogleComputeBackendServiceTlsSettings:
    def __init__(
        self,
        *,
        authentication_config: typing.Optional[builtins.str] = None,
        sni: typing.Optional[builtins.str] = None,
        subject_alt_names: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceTlsSettingsSubjectAltNames", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param authentication_config: Reference to the BackendAuthenticationConfig resource from the networksecurity.googleapis.com namespace. Can be used in authenticating TLS connections to the backend, as specified by the authenticationMode field. Can only be specified if authenticationMode is not NONE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#authentication_config GoogleComputeBackendService#authentication_config}
        :param sni: Server Name Indication - see RFC3546 section 3.1. If set, the load balancer sends this string as the SNI hostname in the TLS connection to the backend, and requires that this string match a Subject Alternative Name (SAN) in the backend's server certificate. With a Regional Internet NEG backend, if the SNI is specified here, the load balancer uses it regardless of whether the Regional Internet NEG is specified with FQDN or IP address and port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#sni GoogleComputeBackendService#sni}
        :param subject_alt_names: subject_alt_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#subject_alt_names GoogleComputeBackendService#subject_alt_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6559f94a5274003a66d6c87643beb1f7a634661af3d6b2ddb084d9f9676eb57)
            check_type(argname="argument authentication_config", value=authentication_config, expected_type=type_hints["authentication_config"])
            check_type(argname="argument sni", value=sni, expected_type=type_hints["sni"])
            check_type(argname="argument subject_alt_names", value=subject_alt_names, expected_type=type_hints["subject_alt_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_config is not None:
            self._values["authentication_config"] = authentication_config
        if sni is not None:
            self._values["sni"] = sni
        if subject_alt_names is not None:
            self._values["subject_alt_names"] = subject_alt_names

    @builtins.property
    def authentication_config(self) -> typing.Optional[builtins.str]:
        '''Reference to the BackendAuthenticationConfig resource from the networksecurity.googleapis.com namespace. Can be used in authenticating TLS connections to the backend, as specified by the authenticationMode field. Can only be specified if authenticationMode is not NONE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#authentication_config GoogleComputeBackendService#authentication_config}
        '''
        result = self._values.get("authentication_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sni(self) -> typing.Optional[builtins.str]:
        '''Server Name Indication - see RFC3546 section 3.1. If set, the load balancer sends this string as the SNI hostname in the TLS connection to the backend, and requires that this string match a Subject Alternative Name (SAN) in the backend's server certificate. With a Regional Internet NEG backend, if the SNI is specified here, the load balancer uses it regardless of whether the Regional Internet NEG is specified with FQDN or IP address and port.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#sni GoogleComputeBackendService#sni}
        '''
        result = self._values.get("sni")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_alt_names(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceTlsSettingsSubjectAltNames"]]]:
        '''subject_alt_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#subject_alt_names GoogleComputeBackendService#subject_alt_names}
        '''
        result = self._values.get("subject_alt_names")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceTlsSettingsSubjectAltNames"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceTlsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceTlsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceTlsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9da66f4e9452d201132101ada4315889aad8cab3abfcd6049b3aca6d6a4f001)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSubjectAltNames")
    def put_subject_alt_names(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeBackendServiceTlsSettingsSubjectAltNames", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4f416a78517fab550bf08f93d74ccdaa73ce0b9d44c837e834002187f2b9a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubjectAltNames", [value]))

    @jsii.member(jsii_name="resetAuthenticationConfig")
    def reset_authentication_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationConfig", []))

    @jsii.member(jsii_name="resetSni")
    def reset_sni(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSni", []))

    @jsii.member(jsii_name="resetSubjectAltNames")
    def reset_subject_alt_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectAltNames", []))

    @builtins.property
    @jsii.member(jsii_name="subjectAltNames")
    def subject_alt_names(
        self,
    ) -> "GoogleComputeBackendServiceTlsSettingsSubjectAltNamesList":
        return typing.cast("GoogleComputeBackendServiceTlsSettingsSubjectAltNamesList", jsii.get(self, "subjectAltNames"))

    @builtins.property
    @jsii.member(jsii_name="authenticationConfigInput")
    def authentication_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sniInput")
    def sni_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sniInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectAltNamesInput")
    def subject_alt_names_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceTlsSettingsSubjectAltNames"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeBackendServiceTlsSettingsSubjectAltNames"]]], jsii.get(self, "subjectAltNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationConfig")
    def authentication_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationConfig"))

    @authentication_config.setter
    def authentication_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c4ad7b11c06da19c70406abde0d6dc97e40d100f789954a949bcb1a1989aa7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sni")
    def sni(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sni"))

    @sni.setter
    def sni(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f96a08f6138964c68132d4dac962e9bc6ded4fb4c9f3021459254fcf5d4de81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sni", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComputeBackendServiceTlsSettings]:
        return typing.cast(typing.Optional[GoogleComputeBackendServiceTlsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeBackendServiceTlsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__843fd21e72fae584c6dae38782fbb7c18a3c9f4316c709dd2f81e286e4ab47f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceTlsSettingsSubjectAltNames",
    jsii_struct_bases=[],
    name_mapping={
        "dns_name": "dnsName",
        "uniform_resource_identifier": "uniformResourceIdentifier",
    },
)
class GoogleComputeBackendServiceTlsSettingsSubjectAltNames:
    def __init__(
        self,
        *,
        dns_name: typing.Optional[builtins.str] = None,
        uniform_resource_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dns_name: The SAN specified as a DNS Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#dns_name GoogleComputeBackendService#dns_name}
        :param uniform_resource_identifier: The SAN specified as a URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#uniform_resource_identifier GoogleComputeBackendService#uniform_resource_identifier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd5d78f4423afbaf0b3752608dd3e65f233556978c1cca35527e95db93fc170b)
            check_type(argname="argument dns_name", value=dns_name, expected_type=type_hints["dns_name"])
            check_type(argname="argument uniform_resource_identifier", value=uniform_resource_identifier, expected_type=type_hints["uniform_resource_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dns_name is not None:
            self._values["dns_name"] = dns_name
        if uniform_resource_identifier is not None:
            self._values["uniform_resource_identifier"] = uniform_resource_identifier

    @builtins.property
    def dns_name(self) -> typing.Optional[builtins.str]:
        '''The SAN specified as a DNS Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#dns_name GoogleComputeBackendService#dns_name}
        '''
        result = self._values.get("dns_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uniform_resource_identifier(self) -> typing.Optional[builtins.str]:
        '''The SAN specified as a URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_backend_service#uniform_resource_identifier GoogleComputeBackendService#uniform_resource_identifier}
        '''
        result = self._values.get("uniform_resource_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeBackendServiceTlsSettingsSubjectAltNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeBackendServiceTlsSettingsSubjectAltNamesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceTlsSettingsSubjectAltNamesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea78ae59629e77cf4e79a525bbbc9734225d3495b4f3817ccab5bb6e12b1235f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeBackendServiceTlsSettingsSubjectAltNamesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee8182886b1834e00ba0b5c3de0614dbefacfc5d482313986aa554051b0e1063)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeBackendServiceTlsSettingsSubjectAltNamesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b732246ab3fb24e2a8f5f686cba8ad4782d84b2ad9d8c1d9fe7a7b95a8a5886)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e94950e3decaf7cdf923ef70b86f161508b7bfda1c9bd9b4931cf7625e4593b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce61db374da7de0c486c1e5f513c0e7b45bbe47a70979cb4584542a72a99bb46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceTlsSettingsSubjectAltNames]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceTlsSettingsSubjectAltNames]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceTlsSettingsSubjectAltNames]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__575c1ece732324e0f7a4c4e33ff4b6928b0deebf46bcecca39568db3ef4e90f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeBackendServiceTlsSettingsSubjectAltNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeBackendService.GoogleComputeBackendServiceTlsSettingsSubjectAltNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bbe2b40b7a66126fc2543e1b95bec103cb207473392c973ab0ba82bdc4c6421)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDnsName")
    def reset_dns_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsName", []))

    @jsii.member(jsii_name="resetUniformResourceIdentifier")
    def reset_uniform_resource_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUniformResourceIdentifier", []))

    @builtins.property
    @jsii.member(jsii_name="dnsNameInput")
    def dns_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsNameInput"))

    @builtins.property
    @jsii.member(jsii_name="uniformResourceIdentifierInput")
    def uniform_resource_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uniformResourceIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsName"))

    @dns_name.setter
    def dns_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__659dd4a52447e06578f7bf57549f1ecfa6a4183c6e78c66d869b19de8d67501d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uniformResourceIdentifier")
    def uniform_resource_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uniformResourceIdentifier"))

    @uniform_resource_identifier.setter
    def uniform_resource_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8998fc5fce0c4e43928dac40a9a60db1fa1e86f1926ef8b942751c5f41eb84cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uniformResourceIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceTlsSettingsSubjectAltNames]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceTlsSettingsSubjectAltNames]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceTlsSettingsSubjectAltNames]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f709a92a034c89b20fe228ce9be6c14f10aec04472100686501c7f6693ecde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeBackendService",
    "GoogleComputeBackendServiceBackend",
    "GoogleComputeBackendServiceBackendCustomMetrics",
    "GoogleComputeBackendServiceBackendCustomMetricsList",
    "GoogleComputeBackendServiceBackendCustomMetricsOutputReference",
    "GoogleComputeBackendServiceBackendList",
    "GoogleComputeBackendServiceBackendOutputReference",
    "GoogleComputeBackendServiceCdnPolicy",
    "GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders",
    "GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersList",
    "GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersOutputReference",
    "GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy",
    "GoogleComputeBackendServiceCdnPolicyCacheKeyPolicyOutputReference",
    "GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy",
    "GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicyList",
    "GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicyOutputReference",
    "GoogleComputeBackendServiceCdnPolicyOutputReference",
    "GoogleComputeBackendServiceCircuitBreakers",
    "GoogleComputeBackendServiceCircuitBreakersConnectTimeout",
    "GoogleComputeBackendServiceCircuitBreakersConnectTimeoutOutputReference",
    "GoogleComputeBackendServiceCircuitBreakersOutputReference",
    "GoogleComputeBackendServiceConfig",
    "GoogleComputeBackendServiceConsistentHash",
    "GoogleComputeBackendServiceConsistentHashHttpCookie",
    "GoogleComputeBackendServiceConsistentHashHttpCookieOutputReference",
    "GoogleComputeBackendServiceConsistentHashHttpCookieTtl",
    "GoogleComputeBackendServiceConsistentHashHttpCookieTtlOutputReference",
    "GoogleComputeBackendServiceConsistentHashOutputReference",
    "GoogleComputeBackendServiceCustomMetrics",
    "GoogleComputeBackendServiceCustomMetricsList",
    "GoogleComputeBackendServiceCustomMetricsOutputReference",
    "GoogleComputeBackendServiceDynamicForwarding",
    "GoogleComputeBackendServiceDynamicForwardingIpPortSelection",
    "GoogleComputeBackendServiceDynamicForwardingIpPortSelectionOutputReference",
    "GoogleComputeBackendServiceDynamicForwardingOutputReference",
    "GoogleComputeBackendServiceIap",
    "GoogleComputeBackendServiceIapOutputReference",
    "GoogleComputeBackendServiceLocalityLbPolicies",
    "GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy",
    "GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicyOutputReference",
    "GoogleComputeBackendServiceLocalityLbPoliciesList",
    "GoogleComputeBackendServiceLocalityLbPoliciesOutputReference",
    "GoogleComputeBackendServiceLocalityLbPoliciesPolicy",
    "GoogleComputeBackendServiceLocalityLbPoliciesPolicyOutputReference",
    "GoogleComputeBackendServiceLogConfig",
    "GoogleComputeBackendServiceLogConfigOutputReference",
    "GoogleComputeBackendServiceMaxStreamDuration",
    "GoogleComputeBackendServiceMaxStreamDurationOutputReference",
    "GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy",
    "GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyOutputReference",
    "GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity",
    "GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinityOutputReference",
    "GoogleComputeBackendServiceOutlierDetection",
    "GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime",
    "GoogleComputeBackendServiceOutlierDetectionBaseEjectionTimeOutputReference",
    "GoogleComputeBackendServiceOutlierDetectionInterval",
    "GoogleComputeBackendServiceOutlierDetectionIntervalOutputReference",
    "GoogleComputeBackendServiceOutlierDetectionOutputReference",
    "GoogleComputeBackendServiceSecuritySettings",
    "GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication",
    "GoogleComputeBackendServiceSecuritySettingsAwsV4AuthenticationOutputReference",
    "GoogleComputeBackendServiceSecuritySettingsOutputReference",
    "GoogleComputeBackendServiceStrongSessionAffinityCookie",
    "GoogleComputeBackendServiceStrongSessionAffinityCookieOutputReference",
    "GoogleComputeBackendServiceStrongSessionAffinityCookieTtl",
    "GoogleComputeBackendServiceStrongSessionAffinityCookieTtlOutputReference",
    "GoogleComputeBackendServiceTimeouts",
    "GoogleComputeBackendServiceTimeoutsOutputReference",
    "GoogleComputeBackendServiceTlsSettings",
    "GoogleComputeBackendServiceTlsSettingsOutputReference",
    "GoogleComputeBackendServiceTlsSettingsSubjectAltNames",
    "GoogleComputeBackendServiceTlsSettingsSubjectAltNamesList",
    "GoogleComputeBackendServiceTlsSettingsSubjectAltNamesOutputReference",
]

publication.publish()

def _typecheckingstub__33c76ef557448049507f2373ae42c7c6fba4f5b6a05fb1e2ecbdb3d2661f976e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    affinity_cookie_ttl_sec: typing.Optional[jsii.Number] = None,
    backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cdn_policy: typing.Optional[typing.Union[GoogleComputeBackendServiceCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    circuit_breakers: typing.Optional[typing.Union[GoogleComputeBackendServiceCircuitBreakers, typing.Dict[builtins.str, typing.Any]]] = None,
    compression_mode: typing.Optional[builtins.str] = None,
    connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
    consistent_hash: typing.Optional[typing.Union[GoogleComputeBackendServiceConsistentHash, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceCustomMetrics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_request_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_response_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamic_forwarding: typing.Optional[typing.Union[GoogleComputeBackendServiceDynamicForwarding, typing.Dict[builtins.str, typing.Any]]] = None,
    edge_security_policy: typing.Optional[builtins.str] = None,
    enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_managed_migration_state: typing.Optional[builtins.str] = None,
    external_managed_migration_testing_percentage: typing.Optional[jsii.Number] = None,
    health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    iap: typing.Optional[typing.Union[GoogleComputeBackendServiceIap, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address_selection_policy: typing.Optional[builtins.str] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    locality_lb_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceLocalityLbPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    locality_lb_policy: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[GoogleComputeBackendServiceLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    max_stream_duration: typing.Optional[typing.Union[GoogleComputeBackendServiceMaxStreamDuration, typing.Dict[builtins.str, typing.Any]]] = None,
    network_pass_through_lb_traffic_policy: typing.Optional[typing.Union[GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    outlier_detection: typing.Optional[typing.Union[GoogleComputeBackendServiceOutlierDetection, typing.Dict[builtins.str, typing.Any]]] = None,
    port_name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    security_policy: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[typing.Union[GoogleComputeBackendServiceSecuritySettings, typing.Dict[builtins.str, typing.Any]]] = None,
    service_lb_policy: typing.Optional[builtins.str] = None,
    session_affinity: typing.Optional[builtins.str] = None,
    strong_session_affinity_cookie: typing.Optional[typing.Union[GoogleComputeBackendServiceStrongSessionAffinityCookie, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeBackendServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_sec: typing.Optional[jsii.Number] = None,
    tls_settings: typing.Optional[typing.Union[GoogleComputeBackendServiceTlsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__313b202239fa6b7a87099322cf9a8af6529f00b1b80682bb4072d1c2489ca9f0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0b0a2be96eef43fdff3354257f1dc0184bd35d0b725da2e7b35336b14cd31f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b5d6b372ea71e815a3055f7b7e1cb687eb607dc36db726ddbc73a236472cca(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceCustomMetrics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d76dee49ea4344eb0e8b2ea3b2d1b342593b4a9381f5cd96cbf16919c8601d1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceLocalityLbPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c300e2c4f51f62750e08bb3e2d7fd306c16423de9fa17017095cf9f51137623(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcde712a72bd8b74cd9514a3c0c1bf27306d896885d219eea4f1f5961af1e48c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19bb873284f5b226c661dc1183d8efdb7bee5e57310689e5e24bc55580587497(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367e37d76bd7701dd5a09716a160d506a8351643ba61ef77109702ba07a1091a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258c384781e18505ba11ca36a4d6ebacbab2d4c6bc8c239e53346dda882c323e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ba96be69dc0480062569dadc94916e2d321a0bc691c0dfae6642740433abd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f974f46a2cd2cfaec39e3d5071fcf1708d32d9391ad2f53a38e8fe1bedc8a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb116baaf0206a1ecef7e00495b404e70f4f3b22ecf13a281ab3ddc45c078a9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb5248c457bc0a76fead84d2c7e02795b64a867d820d62e44affcf6cc0721a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd681836d32e4e8c1b8292d79fc7dd14d086296654349338221783375563b74(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20cd214aa6a29f5b36abf3e67990d28c54a84b05d74bbc3538a466798521dee1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32e3c06b26ec713d3f43159325889b2a271a835f668fef78d7c959f938e3d3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fadcb458461977f9beb50e372ce811e8ab017a32eec95b720b3ef3d74eda022(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a575ba50772d1d1b473ef0708f05a9477058932bc6f9c5915f06050224a8ef31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db726d683c23ce3f3acfb26b584a0448f10857dfa067d14fed88feb51f55371c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531ea69a293cb95d2e490c7df74b02f01f69b92d4d372b1886cb4fed488f3561(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0492687c02726348a8b5cc110b262b90b07f198fb91e942dd8f10c96bdb33790(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b069666c74bf31edd0f973dab2dbec097c78d33f6cc95a6e96e5ad32a0f235c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e0ea2dbcd6666e3e75b86a28118e14169d33c77a7b21f0472858aad708b8d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae5abe296333e27f553c8e4cbb7407e02baa10f7a4cfb8d5c001ea64e15662e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11725d244c105d2224a799fc0dcb1328541ba177df3b101abb4918a624cee2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f60b98e55f3a43e5715dbdd9599eba719ffdb5ad4be58e8f6861df7cb158a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1bca67a9658007c0f4f10d896c644d2f93122728e16ac28d974baaf42ae2124(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbfd99ae8901f9e57b53eff504b4f7e65974875c7fa4fdabdb38e191a57a736(
    *,
    group: builtins.str,
    balancing_mode: typing.Optional[builtins.str] = None,
    capacity_scaler: typing.Optional[jsii.Number] = None,
    custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceBackendCustomMetrics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    max_connections: typing.Optional[jsii.Number] = None,
    max_connections_per_endpoint: typing.Optional[jsii.Number] = None,
    max_connections_per_instance: typing.Optional[jsii.Number] = None,
    max_rate: typing.Optional[jsii.Number] = None,
    max_rate_per_endpoint: typing.Optional[jsii.Number] = None,
    max_rate_per_instance: typing.Optional[jsii.Number] = None,
    max_utilization: typing.Optional[jsii.Number] = None,
    preference: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a6f1f4f3b9709ec0a7016a77db9a051c35ef00ffffc29a63b03b9387baa845(
    *,
    dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    max_utilization: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9960907c3c03704fe8de62e01b753009ee4698120b910d8aa074a353c5d830ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b298b6a6768b051b3b424f28531e42f4426113bc8fdb5d56f2d1c6a84a64358d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__578e62076510a8d024f3b3af6e5794d81ab6f03fe3812c507e79dc068b90d247(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61354b978a729701552d5fcaf8649172e663881ed2c7c9d6cc094044827aaed6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11eb0fc2e1f209e75d6bd89735ddb819eef31f936eecf90fb1b1bdb92ba9ddc2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a765757a197980f30161562769f7bc5045760f6cf0ba271424d47d534083ca6a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceBackendCustomMetrics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf1f42b2150ddc108ad1226744f43154871a3d489807b4d394b6d7ea4162610d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9dffeec3cb92d9c84dc3d7cbc08523db2dbe0dc75cc131e112f28b6e7715294(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2efc037799dcc4035307fbe1530cbb323cb77bb1d2c3a458e4d59683a43671c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96263bdaf506ea81153ea2a1bbaf8b535e534497a36939246f89df0dbab8a0e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4cda6c06f52b533b2c2e246d37d7e7bdaa2df3c1b10c0e40cb3808a815bb5ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceBackendCustomMetrics]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b342bbf483acac495c2d0f9488c97f31c747ceeda3a22c789c91af8ba74b5c8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bbdff86e267f3e46f475381e61bd75f786ceeda155623fd4946805084996a2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e55e4c9e0fa1256d8b974c77beb431005cc8dca53eba70cc5f55e9f2037a1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ef8031e68e54fb271931f3839f049d634a2b3129e1efb61a862c6b378cc7fb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8765e421475e2e13ef2c7db36c13d54a1e34bd71a46e436dc3cb43d044d6f42(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc515253954b3ffe3bdc928dc73c2d40154b56156105f21bb51fab026b5c192(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceBackend]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6035ac3d4e034391ede18081833c249036b3901c0740592a64b2756216c39f84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5efd1f933a766f34c0392287f18d40a9c79382fcf79953b3ac188442008de0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceBackendCustomMetrics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b6ed90e5b8342f491d770b546aea83e39537595609aa18ec8ed851bc79fb253(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4085d986ad88d2cfcdc581231c8b4a99c3a1ef63b23badc0595ab127b306aef2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17515c3740d588a66b894e19e069bac96c0a7cd93f8288b68d25260187e658a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e503fb014457709722374ee1e3a0640bc867df44bae3748b17c1dbc70cedcc36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d80ebbcaedbf05cf5fbdd1ddebedc2ffcc458b8ee30e4c43bd3fae5277d09a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e563af2b3b783d7599e1ecc968adcab29d590edbf21b5a76be77f0a20b07bdd2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39ce97a2bd93ab69db711ea8dcd9508953e3fc9e0488a918eb96c5da27c5beb6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d7f801f813229868841647f8a4e936e913bc27f24b3ca4d94a61e27aba8240(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7850419f9cd5380b97178a3fb7a5bf722bf0b22e8cba15a5c924e38390796316(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed480410089a3ba156071b4b4225480df3b619b92174dcc00d5be46e75d41365(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5613b2f4b00c7394e1066802026aa16e136341b0dd4f5ed15af1985d8562a69f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be35ed0c847204ded352dfa01a5ba0e12bfe1420f8b186b5f6542a2ebdb0ca70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90239351589195c05b9b256bf3960880113b8d29c97f0126866b9e5f809d9d6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceBackend]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2f8d610a7dd12ac6803be451a60d0e7a220ed29b797fae976d0d85e69d4a03(
    *,
    bypass_cache_on_request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cache_key_policy: typing.Optional[typing.Union[GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    cache_mode: typing.Optional[builtins.str] = None,
    client_ttl: typing.Optional[jsii.Number] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    max_ttl: typing.Optional[jsii.Number] = None,
    negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    negative_caching_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_coalescing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    serve_while_stale: typing.Optional[jsii.Number] = None,
    signed_url_cache_max_age_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ac6ff6712f00660947f24b31de8ffa9af037bc4ecacc35b39ee48080300a4c(
    *,
    header_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84be7359d11797331c31f0ca67a28670626526d2e9d30ebd314704316f644595(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d889a18c65001ee804c5407422e71a1a84285d4cd79cb82cb48ce2e511001237(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ab94c6c3b544047b0feaa4c44414e5a98e465998f4475e5a08e529fcf4bffa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8162cd9ba39ffd69e774a024269d5e745100c8d634a123b12615af9747dcd4c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370cb7f826b1e427d3adf56e5194b183c3a3498b341e7db8d9b645a63b207d83(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca10686008a66fc3e9b75ba11f4a4ac5da0e882856b016e38dba4b8087386f3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7cea71d5f57e72d1433a2884ab8f5504ec9bd85fee732be49e68ddf0846425(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e415a66e41e7168c49008ccaf1f9ccb1df036be26a9ca6a01f360469fd965b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8c1b39a13d5048d9781919f9d7e9f29955e55bf63423272d532aaa46edb9f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f91c7c73ed77a18f0de68ad6213b196a738c65e436ee5165db7323e5a1df89(
    *,
    include_host: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_http_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_named_cookies: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_protocol: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_query_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_string_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfd96ca8aaae016391bd054c8f4c5fe9a4044bc1c11344d588d1e3ed1f175b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269c3523464835a9509500bae8114aedca719a0f0dbbb36d75ccdb402d0e7c91(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78cc6e9790b96cc5f6e889833cc1cd39d5047f5176faeca527cfd73816a9e0a1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b047faab6949c5aa771b2b12f8bdbc97972d2e187fc6689f1720c89c97952b0b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb9487a45303a0314c9956d0e80cd20beefc6a966abbe3c73773937b718df60(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d296cca71448a3b351787399d4f1aebff0ae0a3bb760537a34c450ecaccc14f4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea889fbb303af93e913f48d85e08c83d37b29c7bd3d76cbb884f0a0b437d829(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046572159bc53e0243661a621902305a5d21e8a06ed2eff14049bed9c656fdf6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb55b8d4d60a41a5f969e06cd470e1a4874915e9226a4b2f6353d16b725e376c(
    value: typing.Optional[GoogleComputeBackendServiceCdnPolicyCacheKeyPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c74ed9a1649bebae85c400edc899582035d138c5aa97f2b04b08bb8060fcc3f(
    *,
    code: typing.Optional[jsii.Number] = None,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b93c6aad0c0d07cd01145bd38ea2af98d1c61842369cba178d97c4afffb896(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0689d2fb6a4c146b46902281572f28a698316aa413a2980d0a9194d57fa2977(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d2c133203ce230d525c6dd1d8e6099af683b62b85d16650dd7fca68af3074f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e276a2a62c2b234b283fe888d7fe5f5d52dd44dc222d75353aacad8c17cca2a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63da294d021fa65bc5869637eedf4addf6550d5f640315dddd6022d201f8241d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4309394517fee8e849dbf9cef59f0e7eb5ccb235ab8ac519c0d4d5f91f7781(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971bb0642d515d2ef6cab1f24c8aceac3b8b7938d2848b07fd98213c22dc8e5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c72c9b43b3829daa79cd9938d903d18870a7d69cd938bde70d91106a448f7c5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e720ebc76f05ffcb84824a230db7bcdf7242d34fa0be3d3c84fc130ca2f15524(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37cec9c185a1985f3bb0745543060b4bc3a67ee1fcf0966f105b3582c7a5fe1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10d3c5efc43305b60008988789e35b8a80507c801acaf6f0d5f2f8f4f4fac81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07da1a7e6f32856bfae2ed793e5b1d1c25f642e8b46662de3220f5edd42556ba(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5a3a815228ecfaa8d6940c776e06ee53a15c1b602e18a353b4254fd98e0076(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceCdnPolicyNegativeCachingPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517d2102abafd2cc81339ecbb54d8152c53e4c200d6e2d8b537413b7f1fb5ea0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d06cc68283b754add3fcf7935676826df90ca6c60ebb65814f456de603e9cd3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db3e312030792fd997f09e30024112d9467eb8139d1bf62acb66fe5399035071(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0bceea232334d511832d4e2fae3e11e5dd94cbccf076df2c011c5646ad24c43(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8dd85234b72580be5b11f1098fbceead6b51508ddf453552fb5e05b14275fca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3addb66014d29faaf83451e8dd1fdd0099a21c475798fbb34fcf23448dda177e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d096cb83cc27e6a72d15c6563c0a357e03366811663d421be1a6f96f9b1ba02(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624f6d17f505d469677ed77ebb6efbff1c0c1ed4c7aa91dd1b175380d8eb8043(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730760ef13ac64964461c8e9181fed8329cbfeb7f4e7d51194611ab2f0ff8498(
    value: typing.Optional[GoogleComputeBackendServiceCdnPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ddd4c95c404355b1ccf2493eeabb1575b9411b5b898cbec0412b975305346e(
    *,
    connect_timeout: typing.Optional[typing.Union[GoogleComputeBackendServiceCircuitBreakersConnectTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
    max_connections: typing.Optional[jsii.Number] = None,
    max_pending_requests: typing.Optional[jsii.Number] = None,
    max_requests: typing.Optional[jsii.Number] = None,
    max_requests_per_connection: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d2532f0077c762a6af1f071e70525c6930fde0841abc941a1d9e00e1541bc9(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a02802aa3a1adcc3dc53b0abe1d2930c46e424d48805d2005f281285376c0ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf6bfd6c7d8aa557f2226b2c06a74e31bce189c3b143f6c46edb370e3e12384(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc9491401f47b70933ce79267543a58216e35e8464de2c124917b677f892d75(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c63a4e2de79fe986d02eb915986f8bfbf96894242688ee4696344670d07382(
    value: typing.Optional[GoogleComputeBackendServiceCircuitBreakersConnectTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1515814a18c4f8e25e4ff9241dc6e7a5389534d75e473b28a6d2d258afea5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__582b88cc5855defa1573babe95685ca0c4db2687a38522d6514bdb4c208dfc77(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0cd8eb54d7bc0d34daa42c95cbd3cf7c1918b2828b56fab3fd4ec02262c492(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1501b33ac78fbdc1a94099e32e63eb8b5cf5d9c7f43c36221e8282995f35d185(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247a2d7ab5f986c85e353009408e0b61ab29ca4394785671bc901dc507397182(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df499aa6d1f06db0729cb4fac6e0cf295d99245c40077e524a9b8b2b52f354ea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f923395fbe7a9531935d66e17285cb71c20f4dce6b7ab2d9e90ac7bf1a0d190a(
    value: typing.Optional[GoogleComputeBackendServiceCircuitBreakers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed14fbb2abe53b9f287310fcd21c391043238e9e7bc9962b07467d23228cd710(
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
    backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cdn_policy: typing.Optional[typing.Union[GoogleComputeBackendServiceCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    circuit_breakers: typing.Optional[typing.Union[GoogleComputeBackendServiceCircuitBreakers, typing.Dict[builtins.str, typing.Any]]] = None,
    compression_mode: typing.Optional[builtins.str] = None,
    connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
    consistent_hash: typing.Optional[typing.Union[GoogleComputeBackendServiceConsistentHash, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceCustomMetrics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_request_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_response_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamic_forwarding: typing.Optional[typing.Union[GoogleComputeBackendServiceDynamicForwarding, typing.Dict[builtins.str, typing.Any]]] = None,
    edge_security_policy: typing.Optional[builtins.str] = None,
    enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_managed_migration_state: typing.Optional[builtins.str] = None,
    external_managed_migration_testing_percentage: typing.Optional[jsii.Number] = None,
    health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    iap: typing.Optional[typing.Union[GoogleComputeBackendServiceIap, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address_selection_policy: typing.Optional[builtins.str] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    locality_lb_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceLocalityLbPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    locality_lb_policy: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[GoogleComputeBackendServiceLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    max_stream_duration: typing.Optional[typing.Union[GoogleComputeBackendServiceMaxStreamDuration, typing.Dict[builtins.str, typing.Any]]] = None,
    network_pass_through_lb_traffic_policy: typing.Optional[typing.Union[GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    outlier_detection: typing.Optional[typing.Union[GoogleComputeBackendServiceOutlierDetection, typing.Dict[builtins.str, typing.Any]]] = None,
    port_name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    security_policy: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[typing.Union[GoogleComputeBackendServiceSecuritySettings, typing.Dict[builtins.str, typing.Any]]] = None,
    service_lb_policy: typing.Optional[builtins.str] = None,
    session_affinity: typing.Optional[builtins.str] = None,
    strong_session_affinity_cookie: typing.Optional[typing.Union[GoogleComputeBackendServiceStrongSessionAffinityCookie, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeBackendServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_sec: typing.Optional[jsii.Number] = None,
    tls_settings: typing.Optional[typing.Union[GoogleComputeBackendServiceTlsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47ed398189a17dd18841f7f40edd00fb2d882f2bef6d6b8fbc80916bf142337(
    *,
    http_cookie: typing.Optional[typing.Union[GoogleComputeBackendServiceConsistentHashHttpCookie, typing.Dict[builtins.str, typing.Any]]] = None,
    http_header_name: typing.Optional[builtins.str] = None,
    minimum_ring_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0272d3f5627409ca8472996cf123061117bfc99a58951e4c4ebe882a5a52e72c(
    *,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[typing.Union[GoogleComputeBackendServiceConsistentHashHttpCookieTtl, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d511ae43f272b0e25004df9b862cfc235233a0dad3383f334478d52d8d349e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7208c4548dbd9fd3c27fbbda160531eef612002dae4ce84b107a865fac216f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96729fcd20bfea86177bf99d88570a6b349cd153848c9073ced8af1cf6602820(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ed96aa5eab76e1561d9c90b71490cb95574b9f539e600f6937a4c1ebdd4106(
    value: typing.Optional[GoogleComputeBackendServiceConsistentHashHttpCookie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330ccd7c72b76e1018e602374d0d4254b54584a6ea295860ef9d38955a82c32c(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbeb89629142d46d3103b466dcfdde501a3e6c0285f62b9e4f7cd2f4b7fc423(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97070570a117c24be6e0af083be9cf4d80101839f1ccbd4a45d634be0be8979f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654fcbf254b2ddd28bcc2124b72588a327c33f3fec185531e97bca0fe037ce53(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b1274dac7201ff51667bdcf48d6f8905b7fe71c79a2bb62d6b2cbe6dc94aa2(
    value: typing.Optional[GoogleComputeBackendServiceConsistentHashHttpCookieTtl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1addd16f254248f4a269859d6754925e36c340f23ed3bf5f096285ccda07c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c270f3df8ebe44bf8195f9d8c38cfbd49a47cd695d837e335d9f7e4477387f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c07d401d9b283640cf447b05ea553c35e634c0c7618b02bf79b6a1e763af70f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e5bee1008f896b5454c65f5baab95c83810152dea6982fc8beecb9c7b7e0b5(
    value: typing.Optional[GoogleComputeBackendServiceConsistentHash],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21caebe388725dc872106446bd88c969a3ebaf6ac6b3a4370158cb8eda0828c5(
    *,
    dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b53b99188e767122950eabafb030fadc086fa5924b466201bdacd5ec9640330a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90edac07746f5bdbae4395a39de27078ac3d3788732fb2d36e3bca2246c3c36b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24545f976bdcacc2fdeedd4dedc472a115aa68ac5e1732cb12090bfb1021c6e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b873e1a91e5c6c1631ceab9d51c7d9c1378c9e83a22fe364dfecc16247922ed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0731b21e12abe3489add56f226cfd6763a855b8b4968c6e83d1bf3043226ffa5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4e2716c397f72c64e89d3018c03545d8ffc1de08ea5ed061ad481d549ddeda(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceCustomMetrics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f445adb205d7a6b32f609e380ed4423b5854ce262a349f091e33c2f9e4c8ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0500b7eb6493f66540b442437329f3b0a90f1653b1e13b49b62e3c37c33e1c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e45bc4b3d31136fca224c7e8a7d35e6192d65b0a75b326d047a8866d1edb9dbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399e9923df24b22feb284b0f8b74aee218572d5bd59619aa6d61047845a3f922(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceCustomMetrics]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3381437c9f16150ea171c867a5b2548ca4204c6b2f8fe2bfeb5479cd2a681169(
    *,
    ip_port_selection: typing.Optional[typing.Union[GoogleComputeBackendServiceDynamicForwardingIpPortSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395fd8e4734db8b7d226b281732500662906a229429395097325b8c50d035bd5(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327917f90ffb6107496fdba67eb5756a62e6d27d70d55810eede752a4c3a5b91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be473ba8bd849695e2570f9428fcab49c2989df539c8abae9aaa176a28d03160(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ebc0294dc64b37b397e83cdd566fce84b6922e04d2226709f02293af8a06a3(
    value: typing.Optional[GoogleComputeBackendServiceDynamicForwardingIpPortSelection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62e7e0070b9f20920932e2d19c2bd70c1e2ad872d6e35f9ab05bbd7e86dfda0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d768f6adcb50f55b5d7bdd4db35943c8d821ce37bc72017ca6c28cb8d4cf0a75(
    value: typing.Optional[GoogleComputeBackendServiceDynamicForwarding],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120f433cf9d7c6dc483a77a37580b5ba640af33aed515c15ff21140a4f836997(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    oauth2_client_id: typing.Optional[builtins.str] = None,
    oauth2_client_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__379ad90dab79269c462c528995eb5295da18b9064ab1c14032d9f0b164b895b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d611178e7af931cea04a624a86449f45bba959d03b8f9e878c04b5a334b867b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6012b6f127e0a20ec7a9697824ca0ef01205ac2f6d4501c3cd0096de8e8989a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806a62e749148a71abad5018e841827adbdfce1ffb5094cb5eff731be21116d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e76a17569c941f9e8ea3a3f5c1099326483cb2ca1046551ba911f6bec3bd2cd(
    value: typing.Optional[GoogleComputeBackendServiceIap],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1710c9025436d7e4a0453b528d8d71e5b1e18a792c93179b8fec8f47d468c0d(
    *,
    custom_policy: typing.Optional[typing.Union[GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    policy: typing.Optional[typing.Union[GoogleComputeBackendServiceLocalityLbPoliciesPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ade4ddfae6a739c4d6776c5a4dbe2910dbf87d6b3ece8b2fb63cd13269a59f(
    *,
    name: builtins.str,
    data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__778c1abccf536e7718052866e860867a2c78fb9f39372e922be161918f06c7e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f66b37f7bddf91facb74431847d672f5fa5134578345fd24d0e7aad1376e1d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65264707631adc0f19af9be6fc3afb11459d06ca970fd766dcb273d6c2f85251(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac9d8d2bd655a8217d676a840d185c5cd2d255b60e739c8f5f1aa701c67f97b(
    value: typing.Optional[GoogleComputeBackendServiceLocalityLbPoliciesCustomPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285908e2b5af5b4cfa283d3e45df31db15911ba650dd07f59b012be7af92590c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ffcc130faca41dc2782112455a2e0b23981587a37d2d7d71c846b9812f6f91(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a8cc4ae0d3f0c2001351af1b8d09868254fa477180c2518d23e6da01d00fff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b32769f50e7d08e83eccf5bfe0592a6a820db32ef3946ae06c353cb70178a7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4feb3e64b3fb3d35a246187c175f3de71a7141dbee32fe0eefdd9e0dba951026(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db9aa468ab9c4f718abf96386a9085bd22b299158eb3257179c9d51b29d6788(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceLocalityLbPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc5ec9ee35180e228ad623b9bac64d619d0d056c20b25cd3c15ff13f5f3fbb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4356f9c934c17dee85d42a6bd9de981a7056a4f76e0580c5c34bce9fb6e67cc1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceLocalityLbPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d7e43e9ee9ecb81bde5c888d550a2140e75e5d4623bf44426aeec41386d9ee(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b039a9739e928696a172ab45beda86747bf7f2ef43beaedfc490d2fd559ccefa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b1ea765139040773036eaf93caebe771dc5e64d6ddf3684a28def3eae2e3d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb877d742a764a7053174625d039cd4c2253f5eff57f954a9d8572e7a956f837(
    value: typing.Optional[GoogleComputeBackendServiceLocalityLbPoliciesPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de60b5260e5df51352f3d144e6ecc0ffa44de01a5ae46e68a73835bc34cb5f1(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    optional_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    optional_mode: typing.Optional[builtins.str] = None,
    sample_rate: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4208278a042a889d2a2edc354b4aad9db523e97da04d3d0278477dea81a4260(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7722e4377a319d4965eff31e5d53b925f7df0859605b70dad823875e4eb236dc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00465a0936cbed90659fbfa45f0b4457f71628f745d121ede59ffe80d36089e3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f490b272039c35b3e5c8cf5bf0b0b3b1ca4190c3a66e53d8f2dae65fff0b4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9d529cc4bbf82008e3add44c5bf42b4149c72bb05979566201c23a3cec1306(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d33f5e2d4509e50387e91e1e1bfbe6316f3d05146afb92317e759ccd8e2e4a(
    value: typing.Optional[GoogleComputeBackendServiceLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e881db160ff172eaa692d5743b2a5f6a451e13866172ffc6237d3e2512a601a(
    *,
    seconds: builtins.str,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16d109b2489da771d3b2a76bc7f661681f78372a061d4ae11854b35dd91c0af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d94670ec1d52cf76eb3cc701126d7d8dfd7fc47142a2272835f7a141bf899a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b54621a2f2b0f484467d2dd5894c3d298a38ffe2c7b62237bed37c29f89a16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770f8fe692256769e0908712b2836e59ceb53f38b0d44c2b88006e7ff3e84707(
    value: typing.Optional[GoogleComputeBackendServiceMaxStreamDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14206293ac19beb44adb022233c0d77a43a8348745f82aaceb574ce2a5c6caae(
    *,
    zonal_affinity: typing.Optional[typing.Union[GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf74043f85cce4fa359dca4a60cddbdb6a2682c95cd82f265cb3fee7dab8ffc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d2055fb7131780380a8228f0724bb00fd54db3d2a318d76b2220587700e5d3(
    value: typing.Optional[GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d7b901af8f06b4ad0c2e0f0230350ec91fdcb54926da862a918e2af808681b(
    *,
    spillover: typing.Optional[builtins.str] = None,
    spillover_ratio: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9785c09b898c4270814c41f86420506ab95bcd60ea46234594c68c76d7042cd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa8b365f4e4876e35f464ebd546eb5511b8258836b726616a9b29775aa260d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc0cd707c97432df0fbf893fc04c4e6a43ea8cf600397a2bde2d6e7f6156807(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2200260f0e712c48da7708358a8ecdb25460fadd68a5e22a1de86dc1327ce8(
    value: typing.Optional[GoogleComputeBackendServiceNetworkPassThroughLbTrafficPolicyZonalAffinity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f8936a47f2241d620b0584e8298e9238c034306cbf08e400e9c89e7fcf85a3(
    *,
    base_ejection_time: typing.Optional[typing.Union[GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime, typing.Dict[builtins.str, typing.Any]]] = None,
    consecutive_errors: typing.Optional[jsii.Number] = None,
    consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
    enforcing_consecutive_errors: typing.Optional[jsii.Number] = None,
    enforcing_consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
    enforcing_success_rate: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[typing.Union[GoogleComputeBackendServiceOutlierDetectionInterval, typing.Dict[builtins.str, typing.Any]]] = None,
    max_ejection_percent: typing.Optional[jsii.Number] = None,
    success_rate_minimum_hosts: typing.Optional[jsii.Number] = None,
    success_rate_request_volume: typing.Optional[jsii.Number] = None,
    success_rate_stdev_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9709c4013f0d03f53d30f4ca0ab1e74adf7f058a3eb94d2169db29d146d99b2(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88d60875d56dcf455a4e040b9bf4babf9fdbf913ea875f039c81b14261bc09b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__792f01fd4d4c581cf7e95e78cb671e2a5499f823421583f4eebb2e819b6a9dac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e91579c97d1bead8489be5b921cdad4a3687e2c5e2f5262aa7173915267daa3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe0f0affd12e028a305475a77c71756b2b4079f2454f2517c536d8bec660d1b(
    value: typing.Optional[GoogleComputeBackendServiceOutlierDetectionBaseEjectionTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a6701307ce40baffd213c3dee0e59f56bf604db9b680fba438ee80c05917ed4(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e8f0dca10d471e38fb5ad2a5373a6ec54dd0edce88fea129e62d1007d0fcef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80731407ace21a8a501138ad4aaafb43e5605d8e1e31c20b03e741869783d329(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a917cef0c3e11a13047741d244a69a845880cd973e8a984d1ddb7a5126a135da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__058b05c60dd1cc6fc99cfcfdcef7ec3904ff5e68e6f84aab60b080779f03720a(
    value: typing.Optional[GoogleComputeBackendServiceOutlierDetectionInterval],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6884998680063082d1d313ac65b8c62c3ae9db98973823c19d68c372862e956(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ef50129945c3789c215506d579cedd3b52d0c549e900d53e7d99dfc2284f35(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ac30c4abb564c7a7d9c458f1a24fa77c67a6db572d9b75f661bebd007c37f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56678f1c607581870529f669e2827a1f4533b67b13b7bf7b83a94007de7265ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d357fe5dd19f518b63f14bdc51cfcbe084ce9221eeb1aeac9b1aa17c00c498d0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dabc43947cfb61a2580f3c480d99b40d681eed0d83167414ce61b7b676232ddf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb814e298e54c32ce76c5a7f9e54d3e25039b5ded260ce88bd9fb7b5b85d25e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96ba5951aae43be63b5239a13604d0c2267a7dc1b5ee442f5bd683f0ae932fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ac486e53c92c77df7cba602548c549eac8939cd32d117418f5b19352f3ec76(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb25ec655890cdb2019a250f03a4c0924801cb75d82ed54a5b59cc1ad86ee1d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03f98e32708a1da291fe16e3a4117d4df9cd7fcf170cd067a0e0629374e2970(
    value: typing.Optional[GoogleComputeBackendServiceOutlierDetection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d3816b9701dd67e65619dfc27ce28114ba7ab18052ec960bd13eb59f99edfa1(
    *,
    aws_v4_authentication: typing.Optional[typing.Union[GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication, typing.Dict[builtins.str, typing.Any]]] = None,
    client_tls_policy: typing.Optional[builtins.str] = None,
    subject_alt_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9554c4214507ad54b18d225a7ce2131a461d04a30f03513c43f4702d6101e6(
    *,
    access_key: typing.Optional[builtins.str] = None,
    access_key_id: typing.Optional[builtins.str] = None,
    access_key_version: typing.Optional[builtins.str] = None,
    origin_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e2db87ccd39dce4c2e158c8a31bd39fae391a107f5380bb411a34b6eda44f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f6c248559c4091724b7bc22f7f0ae5fbbf1b82d3975e0ef31ffb1ccdca290d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5289b5398d8f75949866d65214dde766d07c8b3ef5443dd39859391849b7c964(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76773eebb2db7da208717870a969c4c8485ff30120468e7ab1622f24da03f6d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a229de67ab6b818c4bac662d31ac5066eed466cc5b1afd8187451d57a3e3b5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047ee8c37d3009b2761b0011f5e5b40a9cf47cc3f05c2185119e6654f151827b(
    value: typing.Optional[GoogleComputeBackendServiceSecuritySettingsAwsV4Authentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a46777b22ae74d280e31514fa2a4101e55bc0a1a77566d63a50f66ae8a0e99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc406aba1aa9fd422913a354556b8d00b652c9d5d784c3d992a40695e9d8a8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a351bc9198d2d66c12cb6b388e9afd52366edecc2f3834c925e01a5d0d365a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7604f7a33ee86ccc1f766a5fc730ea621897b446a3e40f3285a3354e9e929528(
    value: typing.Optional[GoogleComputeBackendServiceSecuritySettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e042d74ead8dd73cdadb9339b61bae63ef850cd6dd1f868605fb315a86452a3d(
    *,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[typing.Union[GoogleComputeBackendServiceStrongSessionAffinityCookieTtl, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a65dbc6a917207f69b79d6e104e77a10017b054d3c33e0f927b979f7226480(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed87dfcae835ec6734ee477bcbd6c2a3a492736802937adc0c9445f5501c606(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de364a6bc0677439b86b18acde300361ab69ba886359f4b710dc952508af7006(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9e833cbd831e3b637541e13461da6597987fe9ad2a4a214d412c2f3afb4aa2(
    value: typing.Optional[GoogleComputeBackendServiceStrongSessionAffinityCookie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a4e718d66eb6c8302aeb36c32a232cb644219c96f6945e51fad10af5c5e0ff4(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144a1cf5595fb0d15b91a054b0f43bd53f7e041c4a15f51ef13c1530bc6e2070(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1dcb2eb5761f9466ce4a2d7820e3261e7bc95cdf8e6ed3dccf9b01ca173d0c3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efea24fdd118f7dc96e3716170da5413a5f6c5f38f44b2094c997940faa5b735(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d83537f59e0e46014925624834a2e8d19da92a5e391caeaeb7aca98678e1ac3(
    value: typing.Optional[GoogleComputeBackendServiceStrongSessionAffinityCookieTtl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b18ff9c68be1dd890a71586f233ee937fc72983ce6b151a8af7508460e92d29(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea63cd71c88d702fe945c899f0dddefda97064d9d9076098f362f00fe2cf5ddf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb5137507cfb605d75429d5173ecaae56ddeaceecdc91f448090af43fb7e224(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3736db3d16224483cabe479b0a0b5ac0701fda430fda59872762fd92cb6de6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d647baad2099f7c57d65a33f008ef8c49f592ca55d8ef444de372ea7704830d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744972ef4963ac7da436a151482f6a8bbe9038c8db20cf2a6b9842c7c09befca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6559f94a5274003a66d6c87643beb1f7a634661af3d6b2ddb084d9f9676eb57(
    *,
    authentication_config: typing.Optional[builtins.str] = None,
    sni: typing.Optional[builtins.str] = None,
    subject_alt_names: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceTlsSettingsSubjectAltNames, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9da66f4e9452d201132101ada4315889aad8cab3abfcd6049b3aca6d6a4f001(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4f416a78517fab550bf08f93d74ccdaa73ce0b9d44c837e834002187f2b9a5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeBackendServiceTlsSettingsSubjectAltNames, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4ad7b11c06da19c70406abde0d6dc97e40d100f789954a949bcb1a1989aa7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f96a08f6138964c68132d4dac962e9bc6ded4fb4c9f3021459254fcf5d4de81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843fd21e72fae584c6dae38782fbb7c18a3c9f4316c709dd2f81e286e4ab47f8(
    value: typing.Optional[GoogleComputeBackendServiceTlsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5d78f4423afbaf0b3752608dd3e65f233556978c1cca35527e95db93fc170b(
    *,
    dns_name: typing.Optional[builtins.str] = None,
    uniform_resource_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea78ae59629e77cf4e79a525bbbc9734225d3495b4f3817ccab5bb6e12b1235f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee8182886b1834e00ba0b5c3de0614dbefacfc5d482313986aa554051b0e1063(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b732246ab3fb24e2a8f5f686cba8ad4782d84b2ad9d8c1d9fe7a7b95a8a5886(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e94950e3decaf7cdf923ef70b86f161508b7bfda1c9bd9b4931cf7625e4593b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce61db374da7de0c486c1e5f513c0e7b45bbe47a70979cb4584542a72a99bb46(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575c1ece732324e0f7a4c4e33ff4b6928b0deebf46bcecca39568db3ef4e90f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeBackendServiceTlsSettingsSubjectAltNames]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbe2b40b7a66126fc2543e1b95bec103cb207473392c973ab0ba82bdc4c6421(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659dd4a52447e06578f7bf57549f1ecfa6a4183c6e78c66d869b19de8d67501d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8998fc5fce0c4e43928dac40a9a60db1fa1e86f1926ef8b942751c5f41eb84cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f709a92a034c89b20fe228ce9be6c14f10aec04472100686501c7f6693ecde(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeBackendServiceTlsSettingsSubjectAltNames]],
) -> None:
    """Type checking stubs"""
    pass
