r'''
# `google_compute_backend_service`

Refer to the Terraform Registry for docs: [`google_compute_backend_service`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service).
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


class ComputeBackendService(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendService",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service google_compute_backend_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        affinity_cookie_ttl_sec: typing.Optional[jsii.Number] = None,
        backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceBackend", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cdn_policy: typing.Optional[typing.Union["ComputeBackendServiceCdnPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        circuit_breakers: typing.Optional[typing.Union["ComputeBackendServiceCircuitBreakers", typing.Dict[builtins.str, typing.Any]]] = None,
        compression_mode: typing.Optional[builtins.str] = None,
        connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
        consistent_hash: typing.Optional[typing.Union["ComputeBackendServiceConsistentHash", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceCustomMetrics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_request_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_response_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        edge_security_policy: typing.Optional[builtins.str] = None,
        enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_managed_migration_state: typing.Optional[builtins.str] = None,
        external_managed_migration_testing_percentage: typing.Optional[jsii.Number] = None,
        health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        iap: typing.Optional[typing.Union["ComputeBackendServiceIap", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address_selection_policy: typing.Optional[builtins.str] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        locality_lb_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceLocalityLbPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        locality_lb_policy: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["ComputeBackendServiceLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        max_stream_duration: typing.Optional[typing.Union["ComputeBackendServiceMaxStreamDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        outlier_detection: typing.Optional[typing.Union["ComputeBackendServiceOutlierDetection", typing.Dict[builtins.str, typing.Any]]] = None,
        port_name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        security_policy: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[typing.Union["ComputeBackendServiceSecuritySettings", typing.Dict[builtins.str, typing.Any]]] = None,
        service_lb_policy: typing.Optional[builtins.str] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        strong_session_affinity_cookie: typing.Optional[typing.Union["ComputeBackendServiceStrongSessionAffinityCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeBackendServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_sec: typing.Optional[jsii.Number] = None,
        tls_settings: typing.Optional[typing.Union["ComputeBackendServiceTlsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service google_compute_backend_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        :param affinity_cookie_ttl_sec: Lifetime of cookies in seconds if session_affinity is GENERATED_COOKIE. If set to 0, the cookie is non-persistent and lasts only until the end of the browser session (or equivalent). The maximum allowed value for TTL is one day. When the load balancing scheme is INTERNAL, this field is not used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#affinity_cookie_ttl_sec ComputeBackendService#affinity_cookie_ttl_sec}
        :param backend: backend block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#backend ComputeBackendService#backend}
        :param cdn_policy: cdn_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#cdn_policy ComputeBackendService#cdn_policy}
        :param circuit_breakers: circuit_breakers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#circuit_breakers ComputeBackendService#circuit_breakers}
        :param compression_mode: Compress text responses using Brotli or gzip compression, based on the client's Accept-Encoding header. Possible values: ["AUTOMATIC", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#compression_mode ComputeBackendService#compression_mode}
        :param connection_draining_timeout_sec: Time for which instance will be drained (not accept new connections, but still work to finish started). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#connection_draining_timeout_sec ComputeBackendService#connection_draining_timeout_sec}
        :param consistent_hash: consistent_hash block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#consistent_hash ComputeBackendService#consistent_hash}
        :param custom_metrics: custom_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#custom_metrics ComputeBackendService#custom_metrics}
        :param custom_request_headers: Headers that the HTTP/S load balancer should add to proxied requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#custom_request_headers ComputeBackendService#custom_request_headers}
        :param custom_response_headers: Headers that the HTTP/S load balancer should add to proxied responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#custom_response_headers ComputeBackendService#custom_response_headers}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#description ComputeBackendService#description}
        :param edge_security_policy: The resource URL for the edge security policy associated with this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#edge_security_policy ComputeBackendService#edge_security_policy}
        :param enable_cdn: If true, enable Cloud CDN for this BackendService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enable_cdn ComputeBackendService#enable_cdn}
        :param external_managed_migration_state: Specifies the canary migration state. Possible values are PREPARE, TEST_BY_PERCENTAGE, and TEST_ALL_TRAFFIC. To begin the migration from EXTERNAL to EXTERNAL_MANAGED, the state must be changed to PREPARE. The state must be changed to TEST_ALL_TRAFFIC before the loadBalancingScheme can be changed to EXTERNAL_MANAGED. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate traffic by percentage using externalManagedMigrationTestingPercentage. Rolling back a migration requires the states to be set in reverse order. So changing the scheme from EXTERNAL_MANAGED to EXTERNAL requires the state to be set to TEST_ALL_TRAFFIC at the same time. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate some traffic back to EXTERNAL or PREPARE can be used to migrate all traffic back to EXTERNAL. Possible values: ["PREPARE", "TEST_BY_PERCENTAGE", "TEST_ALL_TRAFFIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#external_managed_migration_state ComputeBackendService#external_managed_migration_state}
        :param external_managed_migration_testing_percentage: Determines the fraction of requests that should be processed by the Global external Application Load Balancer. The value of this field must be in the range [0, 100]. Session affinity options will slightly affect this routing behavior, for more details, see: Session Affinity. This value can only be set if the loadBalancingScheme in the backend service is set to EXTERNAL (when using the Classic ALB) and the migration state is TEST_BY_PERCENTAGE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#external_managed_migration_testing_percentage ComputeBackendService#external_managed_migration_testing_percentage}
        :param health_checks: The set of URLs to the HttpHealthCheck or HttpsHealthCheck resource for health checking this BackendService. Currently at most one health check can be specified. A health check must be specified unless the backend service uses an internet or serverless NEG as a backend. For internal load balancing, a URL to a HealthCheck resource must be specified instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#health_checks ComputeBackendService#health_checks}
        :param iap: iap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#iap ComputeBackendService#iap}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#id ComputeBackendService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address_selection_policy: Specifies preference of traffic to the backend (from the proxy and from the client for proxyless gRPC). Possible values: ["IPV4_ONLY", "PREFER_IPV6", "IPV6_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#ip_address_selection_policy ComputeBackendService#ip_address_selection_policy}
        :param load_balancing_scheme: Indicates whether the backend service will be used with internal or external load balancing. A backend service created for one type of load balancing cannot be used with the other. For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "INTERNAL_SELF_MANAGED", "INTERNAL_MANAGED", "EXTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#load_balancing_scheme ComputeBackendService#load_balancing_scheme}
        :param locality_lb_policies: locality_lb_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#locality_lb_policies ComputeBackendService#locality_lb_policies}
        :param locality_lb_policy: The load balancing algorithm used within the scope of the locality. The possible values are:. - 'ROUND_ROBIN': This is a simple policy in which each healthy backend is selected in round robin order. - 'LEAST_REQUEST': An O(1) algorithm which selects two random healthy hosts and picks the host which has fewer active requests. - 'RING_HASH': The ring/modulo hash load balancer implements consistent hashing to backends. The algorithm has the property that the addition/removal of a host from a set of N hosts only affects 1/N of the requests. - 'RANDOM': The load balancer selects a random healthy host. - 'ORIGINAL_DESTINATION': Backend host is selected based on the client connection metadata, i.e., connections are opened to the same address as the destination address of the incoming connection before the connection was redirected to the load balancer. - 'MAGLEV': used as a drop in replacement for the ring hash load balancer. Maglev is not as stable as ring hash but has faster table lookup build times and host selection times. For more information about Maglev, refer to https://ai.google/research/pubs/pub44824 - 'WEIGHTED_MAGLEV': Per-instance weighted Load Balancing via health check reported weights. Only applicable to loadBalancingScheme EXTERNAL. If set, the Backend Service must configure a non legacy HTTP-based Health Check, and health check replies are expected to contain non-standard HTTP response header field X-Load-Balancing-Endpoint-Weight to specify the per-instance weights. If set, Load Balancing is weight based on the per-instance weights reported in the last processed health check replies, as long as every instance either reported a valid weight or had UNAVAILABLE_WEIGHT. Otherwise, Load Balancing remains equal-weight. - 'WEIGHTED_ROUND_ROBIN': Per-endpoint weighted round-robin Load Balancing using weights computed from Backend reported Custom Metrics. If set, the Backend Service responses are expected to contain non-standard HTTP response header field X-Endpoint-Load-Metrics. The reported metrics to use for computing the weights are specified via the backends[].customMetrics fields. locality_lb_policy is applicable to either: - A regional backend service with the service_protocol set to HTTP, HTTPS, HTTP2 or H2C, and loadBalancingScheme set to INTERNAL_MANAGED. - A global backend service with the load_balancing_scheme set to INTERNAL_SELF_MANAGED. - A regional backend service with loadBalancingScheme set to EXTERNAL (External Network Load Balancing). Only MAGLEV and WEIGHTED_MAGLEV values are possible for External Network Load Balancing. The default is MAGLEV. If session_affinity is not NONE, and locality_lb_policy is not set to MAGLEV, WEIGHTED_MAGLEV, or RING_HASH, session affinity settings will not take effect. Only ROUND_ROBIN and RING_HASH are supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validate_for_proxyless field set to true. Possible values: ["ROUND_ROBIN", "LEAST_REQUEST", "RING_HASH", "RANDOM", "ORIGINAL_DESTINATION", "MAGLEV", "WEIGHTED_MAGLEV", "WEIGHTED_ROUND_ROBIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#locality_lb_policy ComputeBackendService#locality_lb_policy}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#log_config ComputeBackendService#log_config}
        :param max_stream_duration: max_stream_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_stream_duration ComputeBackendService#max_stream_duration}
        :param outlier_detection: outlier_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#outlier_detection ComputeBackendService#outlier_detection}
        :param port_name: Name of backend port. The same name should appear in the instance groups referenced by this service. Required when the load balancing scheme is EXTERNAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#port_name ComputeBackendService#port_name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#project ComputeBackendService#project}.
        :param protocol: The protocol this BackendService uses to communicate with backends. The default is HTTP. Possible values are HTTP, HTTPS, HTTP2, H2C, TCP, SSL, UDP or GRPC. Refer to the documentation for the load balancers or for Traffic Director for more information. Must be set to GRPC when the backend service is referenced by a URL map that is bound to target gRPC proxy. Possible values: ["HTTP", "HTTPS", "HTTP2", "TCP", "SSL", "UDP", "GRPC", "UNSPECIFIED", "H2C"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#protocol ComputeBackendService#protocol}
        :param security_policy: The security policy associated with this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#security_policy ComputeBackendService#security_policy}
        :param security_settings: security_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#security_settings ComputeBackendService#security_settings}
        :param service_lb_policy: URL to networkservices.ServiceLbPolicy resource. Can only be set if load balancing scheme is EXTERNAL, EXTERNAL_MANAGED, INTERNAL_MANAGED or INTERNAL_SELF_MANAGED and the scope is global. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#service_lb_policy ComputeBackendService#service_lb_policy}
        :param session_affinity: Type of session affinity to use. The default is NONE. Session affinity is not applicable if the protocol is UDP. Possible values: ["NONE", "CLIENT_IP", "CLIENT_IP_PORT_PROTO", "CLIENT_IP_PROTO", "GENERATED_COOKIE", "HEADER_FIELD", "HTTP_COOKIE", "STRONG_COOKIE_AFFINITY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#session_affinity ComputeBackendService#session_affinity}
        :param strong_session_affinity_cookie: strong_session_affinity_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#strong_session_affinity_cookie ComputeBackendService#strong_session_affinity_cookie}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#timeouts ComputeBackendService#timeouts}
        :param timeout_sec: The backend service timeout has a different meaning depending on the type of load balancer. For more information see, `Backend service settings <https://cloud.google.com/compute/docs/reference/rest/v1/backendServices>`_. The default is 30 seconds. The full range of timeout values allowed goes from 1 through 2,147,483,647 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#timeout_sec ComputeBackendService#timeout_sec}
        :param tls_settings: tls_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#tls_settings ComputeBackendService#tls_settings}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec0ba762c0839c825f34e91e5850dc897bb3c707b681b2a918c2b789e193625e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeBackendServiceConfig(
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
        '''Generates CDKTF code for importing a ComputeBackendService resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeBackendService to import.
        :param import_from_id: The id of the existing ComputeBackendService that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeBackendService to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2748e46a5f1b11fa1ba2271f48b0ee6c968a6e438f5ec3d14c413ca8f3e61aa8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackend")
    def put_backend(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceBackend", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631a5ec1d38f4f75cbb4b6564c6085ff926521acb7ffc779f9427ddbc38dfe74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackend", [value]))

    @jsii.member(jsii_name="putCdnPolicy")
    def put_cdn_policy(
        self,
        *,
        bypass_cache_on_request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cache_key_policy: typing.Optional[typing.Union["ComputeBackendServiceCdnPolicyCacheKeyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_mode: typing.Optional[builtins.str] = None,
        client_ttl: typing.Optional[jsii.Number] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        max_ttl: typing.Optional[jsii.Number] = None,
        negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negative_caching_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceCdnPolicyNegativeCachingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_coalescing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        serve_while_stale: typing.Optional[jsii.Number] = None,
        signed_url_cache_max_age_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bypass_cache_on_request_headers: bypass_cache_on_request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#bypass_cache_on_request_headers ComputeBackendService#bypass_cache_on_request_headers}
        :param cache_key_policy: cache_key_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#cache_key_policy ComputeBackendService#cache_key_policy}
        :param cache_mode: Specifies the cache setting for all responses from this backend. The possible values are: USE_ORIGIN_HEADERS, FORCE_CACHE_ALL and CACHE_ALL_STATIC Possible values: ["USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "CACHE_ALL_STATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#cache_mode ComputeBackendService#cache_mode}
        :param client_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#client_ttl ComputeBackendService#client_ttl}
        :param default_ttl: Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#default_ttl ComputeBackendService#default_ttl}
        :param max_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_ttl ComputeBackendService#max_ttl}
        :param negative_caching: Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#negative_caching ComputeBackendService#negative_caching}
        :param negative_caching_policy: negative_caching_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#negative_caching_policy ComputeBackendService#negative_caching_policy}
        :param request_coalescing: If true then Cloud CDN will combine multiple concurrent cache fill requests into a small number of requests to the origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#request_coalescing ComputeBackendService#request_coalescing}
        :param serve_while_stale: Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#serve_while_stale ComputeBackendService#serve_while_stale}
        :param signed_url_cache_max_age_sec: Maximum number of seconds the response to a signed URL request will be considered fresh, defaults to 1hr (3600s). After this time period, the response will be revalidated before being served. When serving responses to signed URL requests, Cloud CDN will internally behave as though all responses from this backend had a "Cache-Control: public, max-age=[TTL]" header, regardless of any existing Cache-Control header. The actual headers served in responses will not be altered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#signed_url_cache_max_age_sec ComputeBackendService#signed_url_cache_max_age_sec}
        '''
        value = ComputeBackendServiceCdnPolicy(
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
        max_connections: typing.Optional[jsii.Number] = None,
        max_pending_requests: typing.Optional[jsii.Number] = None,
        max_requests: typing.Optional[jsii.Number] = None,
        max_requests_per_connection: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_connections: The maximum number of connections to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_connections ComputeBackendService#max_connections}
        :param max_pending_requests: The maximum number of pending requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_pending_requests ComputeBackendService#max_pending_requests}
        :param max_requests: The maximum number of parallel requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_requests ComputeBackendService#max_requests}
        :param max_requests_per_connection: Maximum requests for a single backend connection. This parameter is respected by both the HTTP/1.1 and HTTP/2 implementations. If not specified, there is no limit. Setting this parameter to 1 will effectively disable keep alive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_requests_per_connection ComputeBackendService#max_requests_per_connection}
        :param max_retries: The maximum number of parallel retries to the backend cluster. Defaults to 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_retries ComputeBackendService#max_retries}
        '''
        value = ComputeBackendServiceCircuitBreakers(
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
        http_cookie: typing.Optional[typing.Union["ComputeBackendServiceConsistentHashHttpCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        http_header_name: typing.Optional[builtins.str] = None,
        minimum_ring_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_cookie: http_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#http_cookie ComputeBackendService#http_cookie}
        :param http_header_name: The hash based on the value of the specified header field. This field is applicable if the sessionAffinity is set to HEADER_FIELD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#http_header_name ComputeBackendService#http_header_name}
        :param minimum_ring_size: The minimum number of virtual nodes to use for the hash ring. Larger ring sizes result in more granular load distributions. If the number of hosts in the load balancing pool is larger than the ring size, each host will be assigned a single virtual node. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#minimum_ring_size ComputeBackendService#minimum_ring_size}
        '''
        value = ComputeBackendServiceConsistentHash(
            http_cookie=http_cookie,
            http_header_name=http_header_name,
            minimum_ring_size=minimum_ring_size,
        )

        return typing.cast(None, jsii.invoke(self, "putConsistentHash", [value]))

    @jsii.member(jsii_name="putCustomMetrics")
    def put_custom_metrics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceCustomMetrics", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5ef0aa6cb6aabeed60da75cb71a4342dfca4268b36142979c568209315c2487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomMetrics", [value]))

    @jsii.member(jsii_name="putIap")
    def put_iap(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        oauth2_client_id: typing.Optional[builtins.str] = None,
        oauth2_client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Whether the serving infrastructure will authenticate and authorize all incoming requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enabled ComputeBackendService#enabled}
        :param oauth2_client_id: OAuth2 Client ID for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#oauth2_client_id ComputeBackendService#oauth2_client_id}
        :param oauth2_client_secret: OAuth2 Client Secret for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#oauth2_client_secret ComputeBackendService#oauth2_client_secret}
        '''
        value = ComputeBackendServiceIap(
            enabled=enabled,
            oauth2_client_id=oauth2_client_id,
            oauth2_client_secret=oauth2_client_secret,
        )

        return typing.cast(None, jsii.invoke(self, "putIap", [value]))

    @jsii.member(jsii_name="putLocalityLbPolicies")
    def put_locality_lb_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceLocalityLbPolicies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4f78adc1b10b49ad21baa275b9bd5c83c4cdcd7da4e3c6662b0024ad166af58)
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
        :param enable: Whether to enable logging for the load balancer traffic served by this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enable ComputeBackendService#enable}
        :param optional_fields: This field can only be specified if logging is enabled for this backend service and "logConfig.optionalMode" was set to CUSTOM. Contains a list of optional fields you want to include in the logs. For example: serverInstance, serverGkeDetails.cluster, serverGkeDetails.pod.podNamespace For example: orca_load_report, tls.protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#optional_fields ComputeBackendService#optional_fields}
        :param optional_mode: Specifies the optional logging mode for the load balancer traffic. Supported values: INCLUDE_ALL_OPTIONAL, EXCLUDE_ALL_OPTIONAL, CUSTOM. Possible values: ["INCLUDE_ALL_OPTIONAL", "EXCLUDE_ALL_OPTIONAL", "CUSTOM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#optional_mode ComputeBackendService#optional_mode}
        :param sample_rate: This field can only be specified if logging is enabled for this backend service. The value of the field must be in [0, 1]. This configures the sampling rate of requests to the load balancer where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported. The default value is 1.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#sample_rate ComputeBackendService#sample_rate}
        '''
        value = ComputeBackendServiceLogConfig(
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. (int64 format). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#seconds ComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#nanos ComputeBackendService#nanos}
        '''
        value = ComputeBackendServiceMaxStreamDuration(seconds=seconds, nanos=nanos)

        return typing.cast(None, jsii.invoke(self, "putMaxStreamDuration", [value]))

    @jsii.member(jsii_name="putOutlierDetection")
    def put_outlier_detection(
        self,
        *,
        base_ejection_time: typing.Optional[typing.Union["ComputeBackendServiceOutlierDetectionBaseEjectionTime", typing.Dict[builtins.str, typing.Any]]] = None,
        consecutive_errors: typing.Optional[jsii.Number] = None,
        consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_errors: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_success_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[typing.Union["ComputeBackendServiceOutlierDetectionInterval", typing.Dict[builtins.str, typing.Any]]] = None,
        max_ejection_percent: typing.Optional[jsii.Number] = None,
        success_rate_minimum_hosts: typing.Optional[jsii.Number] = None,
        success_rate_request_volume: typing.Optional[jsii.Number] = None,
        success_rate_stdev_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param base_ejection_time: base_ejection_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#base_ejection_time ComputeBackendService#base_ejection_time}
        :param consecutive_errors: Number of errors before a host is ejected from the connection pool. When the backend host is accessed over HTTP, a 5xx return code qualifies as an error. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#consecutive_errors ComputeBackendService#consecutive_errors}
        :param consecutive_gateway_failure: The number of consecutive gateway failures (502, 503, 504 status or connection errors that are mapped to one of those status codes) before a consecutive gateway failure ejection occurs. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#consecutive_gateway_failure ComputeBackendService#consecutive_gateway_failure}
        :param enforcing_consecutive_errors: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive 5xx. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enforcing_consecutive_errors ComputeBackendService#enforcing_consecutive_errors}
        :param enforcing_consecutive_gateway_failure: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive gateway failures. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enforcing_consecutive_gateway_failure ComputeBackendService#enforcing_consecutive_gateway_failure}
        :param enforcing_success_rate: The percentage chance that a host will be actually ejected when an outlier status is detected through success rate statistics. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enforcing_success_rate ComputeBackendService#enforcing_success_rate}
        :param interval: interval block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#interval ComputeBackendService#interval}
        :param max_ejection_percent: Maximum percentage of hosts in the load balancing pool for the backend service that can be ejected. Defaults to 10%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_ejection_percent ComputeBackendService#max_ejection_percent}
        :param success_rate_minimum_hosts: The number of hosts in a cluster that must have enough request volume to detect success rate outliers. If the number of hosts is less than this setting, outlier detection via success rate statistics is not performed for any host in the cluster. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#success_rate_minimum_hosts ComputeBackendService#success_rate_minimum_hosts}
        :param success_rate_request_volume: The minimum number of total requests that must be collected in one interval (as defined by the interval duration above) to include this host in success rate based outlier detection. If the volume is lower than this setting, outlier detection via success rate statistics is not performed for that host. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#success_rate_request_volume ComputeBackendService#success_rate_request_volume}
        :param success_rate_stdev_factor: This factor is used to determine the ejection threshold for success rate outlier ejection. The ejection threshold is the difference between the mean success rate, and the product of this factor and the standard deviation of the mean success rate: mean - (stdev * success_rate_stdev_factor). This factor is divided by a thousand to get a double. That is, if the desired factor is 1.9, the runtime value should be 1900. Defaults to 1900. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#success_rate_stdev_factor ComputeBackendService#success_rate_stdev_factor}
        '''
        value = ComputeBackendServiceOutlierDetection(
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
        aws_v4_authentication: typing.Optional[typing.Union["ComputeBackendServiceSecuritySettingsAwsV4Authentication", typing.Dict[builtins.str, typing.Any]]] = None,
        client_tls_policy: typing.Optional[builtins.str] = None,
        subject_alt_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param aws_v4_authentication: aws_v4_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#aws_v4_authentication ComputeBackendService#aws_v4_authentication}
        :param client_tls_policy: ClientTlsPolicy is a resource that specifies how a client should authenticate connections to backends of a service. This resource itself does not affect configuration unless it is attached to a backend service resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#client_tls_policy ComputeBackendService#client_tls_policy}
        :param subject_alt_names: A list of alternate names to verify the subject identity in the certificate. If specified, the client will verify that the server certificate's subject alt name matches one of the specified values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#subject_alt_names ComputeBackendService#subject_alt_names}
        '''
        value = ComputeBackendServiceSecuritySettings(
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
        ttl: typing.Optional[typing.Union["ComputeBackendServiceStrongSessionAffinityCookieTtl", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#path ComputeBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#ttl ComputeBackendService#ttl}
        '''
        value = ComputeBackendServiceStrongSessionAffinityCookie(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#create ComputeBackendService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#delete ComputeBackendService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#update ComputeBackendService#update}.
        '''
        value = ComputeBackendServiceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTlsSettings")
    def put_tls_settings(
        self,
        *,
        authentication_config: typing.Optional[builtins.str] = None,
        sni: typing.Optional[builtins.str] = None,
        subject_alt_names: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceTlsSettingsSubjectAltNames", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param authentication_config: Reference to the BackendAuthenticationConfig resource from the networksecurity.googleapis.com namespace. Can be used in authenticating TLS connections to the backend, as specified by the authenticationMode field. Can only be specified if authenticationMode is not NONE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#authentication_config ComputeBackendService#authentication_config}
        :param sni: Server Name Indication - see RFC3546 section 3.1. If set, the load balancer sends this string as the SNI hostname in the TLS connection to the backend, and requires that this string match a Subject Alternative Name (SAN) in the backend's server certificate. With a Regional Internet NEG backend, if the SNI is specified here, the load balancer uses it regardless of whether the Regional Internet NEG is specified with FQDN or IP address and port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#sni ComputeBackendService#sni}
        :param subject_alt_names: subject_alt_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#subject_alt_names ComputeBackendService#subject_alt_names}
        '''
        value = ComputeBackendServiceTlsSettings(
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
    def backend(self) -> "ComputeBackendServiceBackendList":
        return typing.cast("ComputeBackendServiceBackendList", jsii.get(self, "backend"))

    @builtins.property
    @jsii.member(jsii_name="cdnPolicy")
    def cdn_policy(self) -> "ComputeBackendServiceCdnPolicyOutputReference":
        return typing.cast("ComputeBackendServiceCdnPolicyOutputReference", jsii.get(self, "cdnPolicy"))

    @builtins.property
    @jsii.member(jsii_name="circuitBreakers")
    def circuit_breakers(self) -> "ComputeBackendServiceCircuitBreakersOutputReference":
        return typing.cast("ComputeBackendServiceCircuitBreakersOutputReference", jsii.get(self, "circuitBreakers"))

    @builtins.property
    @jsii.member(jsii_name="consistentHash")
    def consistent_hash(self) -> "ComputeBackendServiceConsistentHashOutputReference":
        return typing.cast("ComputeBackendServiceConsistentHashOutputReference", jsii.get(self, "consistentHash"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="customMetrics")
    def custom_metrics(self) -> "ComputeBackendServiceCustomMetricsList":
        return typing.cast("ComputeBackendServiceCustomMetricsList", jsii.get(self, "customMetrics"))

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
    def iap(self) -> "ComputeBackendServiceIapOutputReference":
        return typing.cast("ComputeBackendServiceIapOutputReference", jsii.get(self, "iap"))

    @builtins.property
    @jsii.member(jsii_name="localityLbPolicies")
    def locality_lb_policies(self) -> "ComputeBackendServiceLocalityLbPoliciesList":
        return typing.cast("ComputeBackendServiceLocalityLbPoliciesList", jsii.get(self, "localityLbPolicies"))

    @builtins.property
    @jsii.member(jsii_name="logConfig")
    def log_config(self) -> "ComputeBackendServiceLogConfigOutputReference":
        return typing.cast("ComputeBackendServiceLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="maxStreamDuration")
    def max_stream_duration(
        self,
    ) -> "ComputeBackendServiceMaxStreamDurationOutputReference":
        return typing.cast("ComputeBackendServiceMaxStreamDurationOutputReference", jsii.get(self, "maxStreamDuration"))

    @builtins.property
    @jsii.member(jsii_name="outlierDetection")
    def outlier_detection(
        self,
    ) -> "ComputeBackendServiceOutlierDetectionOutputReference":
        return typing.cast("ComputeBackendServiceOutlierDetectionOutputReference", jsii.get(self, "outlierDetection"))

    @builtins.property
    @jsii.member(jsii_name="securitySettings")
    def security_settings(
        self,
    ) -> "ComputeBackendServiceSecuritySettingsOutputReference":
        return typing.cast("ComputeBackendServiceSecuritySettingsOutputReference", jsii.get(self, "securitySettings"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="strongSessionAffinityCookie")
    def strong_session_affinity_cookie(
        self,
    ) -> "ComputeBackendServiceStrongSessionAffinityCookieOutputReference":
        return typing.cast("ComputeBackendServiceStrongSessionAffinityCookieOutputReference", jsii.get(self, "strongSessionAffinityCookie"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeBackendServiceTimeoutsOutputReference":
        return typing.cast("ComputeBackendServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="tlsSettings")
    def tls_settings(self) -> "ComputeBackendServiceTlsSettingsOutputReference":
        return typing.cast("ComputeBackendServiceTlsSettingsOutputReference", jsii.get(self, "tlsSettings"))

    @builtins.property
    @jsii.member(jsii_name="affinityCookieTtlSecInput")
    def affinity_cookie_ttl_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "affinityCookieTtlSecInput"))

    @builtins.property
    @jsii.member(jsii_name="backendInput")
    def backend_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceBackend"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceBackend"]]], jsii.get(self, "backendInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnPolicyInput")
    def cdn_policy_input(self) -> typing.Optional["ComputeBackendServiceCdnPolicy"]:
        return typing.cast(typing.Optional["ComputeBackendServiceCdnPolicy"], jsii.get(self, "cdnPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="circuitBreakersInput")
    def circuit_breakers_input(
        self,
    ) -> typing.Optional["ComputeBackendServiceCircuitBreakers"]:
        return typing.cast(typing.Optional["ComputeBackendServiceCircuitBreakers"], jsii.get(self, "circuitBreakersInput"))

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
    ) -> typing.Optional["ComputeBackendServiceConsistentHash"]:
        return typing.cast(typing.Optional["ComputeBackendServiceConsistentHash"], jsii.get(self, "consistentHashInput"))

    @builtins.property
    @jsii.member(jsii_name="customMetricsInput")
    def custom_metrics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceCustomMetrics"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceCustomMetrics"]]], jsii.get(self, "customMetricsInput"))

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
    def iap_input(self) -> typing.Optional["ComputeBackendServiceIap"]:
        return typing.cast(typing.Optional["ComputeBackendServiceIap"], jsii.get(self, "iapInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceLocalityLbPolicies"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceLocalityLbPolicies"]]], jsii.get(self, "localityLbPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="localityLbPolicyInput")
    def locality_lb_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localityLbPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigInput")
    def log_config_input(self) -> typing.Optional["ComputeBackendServiceLogConfig"]:
        return typing.cast(typing.Optional["ComputeBackendServiceLogConfig"], jsii.get(self, "logConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="maxStreamDurationInput")
    def max_stream_duration_input(
        self,
    ) -> typing.Optional["ComputeBackendServiceMaxStreamDuration"]:
        return typing.cast(typing.Optional["ComputeBackendServiceMaxStreamDuration"], jsii.get(self, "maxStreamDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="outlierDetectionInput")
    def outlier_detection_input(
        self,
    ) -> typing.Optional["ComputeBackendServiceOutlierDetection"]:
        return typing.cast(typing.Optional["ComputeBackendServiceOutlierDetection"], jsii.get(self, "outlierDetectionInput"))

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
    ) -> typing.Optional["ComputeBackendServiceSecuritySettings"]:
        return typing.cast(typing.Optional["ComputeBackendServiceSecuritySettings"], jsii.get(self, "securitySettingsInput"))

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
    ) -> typing.Optional["ComputeBackendServiceStrongSessionAffinityCookie"]:
        return typing.cast(typing.Optional["ComputeBackendServiceStrongSessionAffinityCookie"], jsii.get(self, "strongSessionAffinityCookieInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecInput")
    def timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeBackendServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeBackendServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsSettingsInput")
    def tls_settings_input(self) -> typing.Optional["ComputeBackendServiceTlsSettings"]:
        return typing.cast(typing.Optional["ComputeBackendServiceTlsSettings"], jsii.get(self, "tlsSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="affinityCookieTtlSec")
    def affinity_cookie_ttl_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "affinityCookieTtlSec"))

    @affinity_cookie_ttl_sec.setter
    def affinity_cookie_ttl_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96824ed5070e5bc7c1fe7684179435ad257b61c951431ce34b9111ce189e749d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "affinityCookieTtlSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="compressionMode")
    def compression_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionMode"))

    @compression_mode.setter
    def compression_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0277052f737abc2533ae00a964194ffd53dfbe7202155760975927d59ab8e078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionDrainingTimeoutSec")
    def connection_draining_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectionDrainingTimeoutSec"))

    @connection_draining_timeout_sec.setter
    def connection_draining_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9371ee8707a446a33b3e876187c64c99640dc11d0ed107d4bffc83fd9883386c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionDrainingTimeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customRequestHeaders")
    def custom_request_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customRequestHeaders"))

    @custom_request_headers.setter
    def custom_request_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__659607ed2adf1a596de18e4359763d847c01c4652b97fe29de1e1326c45f95ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customRequestHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customResponseHeaders")
    def custom_response_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customResponseHeaders"))

    @custom_response_headers.setter
    def custom_response_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70aa0e8a68885d80c7d14a4f4c4bab18abcccde29f2192536bb33d1228b652e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customResponseHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc84704b7a4b0151f9470b0aefbca9d96555a281d2905a039f76177a909a4c49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgeSecurityPolicy")
    def edge_security_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeSecurityPolicy"))

    @edge_security_policy.setter
    def edge_security_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4d43e84f92249c0b68a9ae09de31007c6570a15f3b0c3a6a982676b8bb7120)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cb984aefa5d195c2d7b6bbaa9c768a24d1f00fa5a25d25396b5cb063ec6f0b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableCdn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalManagedMigrationState")
    def external_managed_migration_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalManagedMigrationState"))

    @external_managed_migration_state.setter
    def external_managed_migration_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__943a85e01dce9020e3a0b46ccd264ff8a616b979e64d00017ec3cc7ae337765c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalManagedMigrationState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalManagedMigrationTestingPercentage")
    def external_managed_migration_testing_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "externalManagedMigrationTestingPercentage"))

    @external_managed_migration_testing_percentage.setter
    def external_managed_migration_testing_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6390a8d6cb61a4ee9828c27a8e78eb83e199a39970cddc7adc3681d04a98f15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalManagedMigrationTestingPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthChecks")
    def health_checks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "healthChecks"))

    @health_checks.setter
    def health_checks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daf788042dd6bcd1a9ef797db0560897efba15a0fec845b3330006d80360bb3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthChecks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07e8c5f4cc9939a8cc198d1601862b423743ea12887ed6bef51560413942c9e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddressSelectionPolicy")
    def ip_address_selection_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressSelectionPolicy"))

    @ip_address_selection_policy.setter
    def ip_address_selection_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f656c35dca2fa5a40d787284ba916655faed6a5ac132fa04cde7ad5b58ba16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressSelectionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingScheme")
    def load_balancing_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingScheme"))

    @load_balancing_scheme.setter
    def load_balancing_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd27edef7e41c782e02d88cf732d20735003608594bdb4c67e9278214cc5179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingScheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localityLbPolicy")
    def locality_lb_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localityLbPolicy"))

    @locality_lb_policy.setter
    def locality_lb_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f07b9cdcb580bc07591873aafb0dc2031115cc12034d85d511a454c09570822f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localityLbPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8548951e1e243230e4d3b0fc8d0a7b7e7a6699b56dddbdc3959aea9e081bac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a8b380663fc71718af8470b0765dc139eabb53e0a08e9cf4b4a97daf5842a84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15c93603bc8c05e2929700e323e7049a582ca0d9bba4d8212d44cf2430ecd8ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad1ad86e088065fb20fdc2550806001a398faeb243eebb41ab2729e69ad6da9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityPolicy")
    def security_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityPolicy"))

    @security_policy.setter
    def security_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2397033856c88700a891fd41e8b8279604c2b69b8d243f621ca5d545b21734d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceLbPolicy")
    def service_lb_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceLbPolicy"))

    @service_lb_policy.setter
    def service_lb_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f0801892c026015de994a9cbd6ec9ca0bcdda320dc4d68de0806b2e0e87c0ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceLbPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionAffinity")
    def session_affinity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionAffinity"))

    @session_affinity.setter
    def session_affinity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083b6be75668e7f751a48bc2e3c41e16d16f0c7d65535be29464a5d66402ac54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSec")
    def timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSec"))

    @timeout_sec.setter
    def timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014c9f4b87f03952f5215685606fbba530932ac0fbf4e40126e32ef4ecbb2d70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSec", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceBackend",
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
class ComputeBackendServiceBackend:
    def __init__(
        self,
        *,
        group: builtins.str,
        balancing_mode: typing.Optional[builtins.str] = None,
        capacity_scaler: typing.Optional[jsii.Number] = None,
        custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceBackendCustomMetrics", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param group: The fully-qualified URL of an Instance Group or Network Endpoint Group resource. In case of instance group this defines the list of instances that serve traffic. Member virtual machine instances from each instance group must live in the same zone as the instance group itself. No two backends in a backend service are allowed to use same Instance Group resource. For Network Endpoint Groups this defines list of endpoints. All endpoints of Network Endpoint Group must be hosted on instances located in the same zone as the Network Endpoint Group. Backend services cannot mix Instance Group and Network Endpoint Group backends. Note that you must specify an Instance Group or Network Endpoint Group resource using the fully-qualified URL, rather than a partial URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#group ComputeBackendService#group}
        :param balancing_mode: Specifies the balancing mode for this backend. For global HTTP(S) or TCP/SSL load balancing, the default is UTILIZATION. Valid values are UTILIZATION, RATE (for HTTP(S)), CUSTOM_METRICS (for HTTP(s)) and CONNECTION (for TCP/SSL). See the `Backend Services Overview <https://cloud.google.com/load-balancing/docs/backend-service#balancing-mode>`_ for an explanation of load balancing modes. Default value: "UTILIZATION" Possible values: ["UTILIZATION", "RATE", "CONNECTION", "CUSTOM_METRICS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#balancing_mode ComputeBackendService#balancing_mode}
        :param capacity_scaler: A multiplier applied to the group's maximum servicing capacity (based on UTILIZATION, RATE or CONNECTION). Default value is 1, which means the group will serve up to 100% of its configured capacity (depending on balancingMode). A setting of 0 means the group is completely drained, offering 0% of its available Capacity. Valid range is [0.0,1.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#capacity_scaler ComputeBackendService#capacity_scaler}
        :param custom_metrics: custom_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#custom_metrics ComputeBackendService#custom_metrics}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#description ComputeBackendService#description}
        :param max_connections: The max number of simultaneous connections for the group. Can be used with either CONNECTION or UTILIZATION balancing modes. For CONNECTION mode, either maxConnections or one of maxConnectionsPerInstance or maxConnectionsPerEndpoint, as appropriate for group type, must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_connections ComputeBackendService#max_connections}
        :param max_connections_per_endpoint: The max number of simultaneous connections that a single backend network endpoint can handle. This is used to calculate the capacity of the group. Can be used in either CONNECTION or UTILIZATION balancing modes. For CONNECTION mode, either maxConnections or maxConnectionsPerEndpoint must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_connections_per_endpoint ComputeBackendService#max_connections_per_endpoint}
        :param max_connections_per_instance: The max number of simultaneous connections that a single backend instance can handle. This is used to calculate the capacity of the group. Can be used in either CONNECTION or UTILIZATION balancing modes. For CONNECTION mode, either maxConnections or maxConnectionsPerInstance must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_connections_per_instance ComputeBackendService#max_connections_per_instance}
        :param max_rate: The max requests per second (RPS) of the group. Can be used with either RATE or UTILIZATION balancing modes, but required if RATE mode. For RATE mode, either maxRate or one of maxRatePerInstance or maxRatePerEndpoint, as appropriate for group type, must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_rate ComputeBackendService#max_rate}
        :param max_rate_per_endpoint: The max requests per second (RPS) that a single backend network endpoint can handle. This is used to calculate the capacity of the group. Can be used in either balancing mode. For RATE mode, either maxRate or maxRatePerEndpoint must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_rate_per_endpoint ComputeBackendService#max_rate_per_endpoint}
        :param max_rate_per_instance: The max requests per second (RPS) that a single backend instance can handle. This is used to calculate the capacity of the group. Can be used in either balancing mode. For RATE mode, either maxRate or maxRatePerInstance must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_rate_per_instance ComputeBackendService#max_rate_per_instance}
        :param max_utilization: Used when balancingMode is UTILIZATION. This ratio defines the CPU utilization target for the group. Valid range is [0.0, 1.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_utilization ComputeBackendService#max_utilization}
        :param preference: This field indicates whether this backend should be fully utilized before sending traffic to backends with default preference. This field cannot be set when loadBalancingScheme is set to 'EXTERNAL'. The possible values are: - PREFERRED: Backends with this preference level will be filled up to their capacity limits first, based on RTT. - DEFAULT: If preferred backends don't have enough capacity, backends in this layer would be used and traffic would be assigned based on the load balancing algorithm you use. This is the default Possible values: ["PREFERRED", "DEFAULT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#preference ComputeBackendService#preference}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1712d6d29dcdd70242b1931e30d2669f08eb7cdd6eee53142eda9a5d79ccfce0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#group ComputeBackendService#group}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#balancing_mode ComputeBackendService#balancing_mode}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#capacity_scaler ComputeBackendService#capacity_scaler}
        '''
        result = self._values.get("capacity_scaler")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_metrics(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceBackendCustomMetrics"]]]:
        '''custom_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#custom_metrics ComputeBackendService#custom_metrics}
        '''
        result = self._values.get("custom_metrics")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceBackendCustomMetrics"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#description ComputeBackendService#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_connections(self) -> typing.Optional[jsii.Number]:
        '''The max number of simultaneous connections for the group. Can be used with either CONNECTION or UTILIZATION balancing modes.

        For CONNECTION mode, either maxConnections or one
        of maxConnectionsPerInstance or maxConnectionsPerEndpoint,
        as appropriate for group type, must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_connections ComputeBackendService#max_connections}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_connections_per_endpoint ComputeBackendService#max_connections_per_endpoint}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_connections_per_instance ComputeBackendService#max_connections_per_instance}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_rate ComputeBackendService#max_rate}
        '''
        result = self._values.get("max_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_rate_per_endpoint(self) -> typing.Optional[jsii.Number]:
        '''The max requests per second (RPS) that a single backend network endpoint can handle.

        This is used to calculate the capacity of
        the group. Can be used in either balancing mode. For RATE mode,
        either maxRate or maxRatePerEndpoint must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_rate_per_endpoint ComputeBackendService#max_rate_per_endpoint}
        '''
        result = self._values.get("max_rate_per_endpoint")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_rate_per_instance(self) -> typing.Optional[jsii.Number]:
        '''The max requests per second (RPS) that a single backend instance can handle.

        This is used to calculate the capacity of
        the group. Can be used in either balancing mode. For RATE mode,
        either maxRate or maxRatePerInstance must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_rate_per_instance ComputeBackendService#max_rate_per_instance}
        '''
        result = self._values.get("max_rate_per_instance")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_utilization(self) -> typing.Optional[jsii.Number]:
        '''Used when balancingMode is UTILIZATION. This ratio defines the CPU utilization target for the group. Valid range is [0.0, 1.0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_utilization ComputeBackendService#max_utilization}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#preference ComputeBackendService#preference}
        '''
        result = self._values.get("preference")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceBackend(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceBackendCustomMetrics",
    jsii_struct_bases=[],
    name_mapping={
        "dry_run": "dryRun",
        "name": "name",
        "max_utilization": "maxUtilization",
    },
)
class ComputeBackendServiceBackendCustomMetrics:
    def __init__(
        self,
        *,
        dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        max_utilization: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param dry_run: If true, the metric data is collected and reported to Cloud Monitoring, but is not used for load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#dry_run ComputeBackendService#dry_run}
        :param name: Name of a custom utilization signal. The name must be 1-64 characters long and match the regular expression `a-z <%5B-_.a-z0-9%5D*%5Ba-z0-9%5D>`_? which means the first character must be a lowercase letter, and all following characters must be a dash, period, underscore, lowercase letter, or digit, except the last character, which cannot be a dash, period, or underscore. For usage guidelines, see Custom Metrics balancing mode. This field can only be used for a global or regional backend service with the loadBalancingScheme set to EXTERNAL_MANAGED, INTERNAL_MANAGED INTERNAL_SELF_MANAGED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        :param max_utilization: Optional parameter to define a target utilization for the Custom Metrics balancing mode. The valid range is [0.0, 1.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_utilization ComputeBackendService#max_utilization}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f956c7990787600049c6b19be0d39c889b45954e5c7f063b5b136db3c8fbd6d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#dry_run ComputeBackendService#dry_run}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_utilization(self) -> typing.Optional[jsii.Number]:
        '''Optional parameter to define a target utilization for the Custom Metrics balancing mode. The valid range is [0.0, 1.0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_utilization ComputeBackendService#max_utilization}
        '''
        result = self._values.get("max_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceBackendCustomMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceBackendCustomMetricsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceBackendCustomMetricsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04d8d2db6abd80a289e69176073682a1409281312a4c2a864133adc3a638f477)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeBackendServiceBackendCustomMetricsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__065f8bed6797bb1df12d942873aea7e190bc435e4296920df8cbb9b3daa04301)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeBackendServiceBackendCustomMetricsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3cd34ea164c95b4e3fceac427344511254dcc66671651a79aaab18bceebad7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1481940813e8f9e997b96c147b5ae1df8ad68bd457313f52344054156d26a2c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__036ba400966c06aa7f211ab1df36f7fb04c4c55885d96bca4b50dd34e3bd8c19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceBackendCustomMetrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceBackendCustomMetrics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceBackendCustomMetrics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716ee0f85fd48565484c4d3494880f8c355cac7b8e57f03da634d1e1db742702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendServiceBackendCustomMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceBackendCustomMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38915529b79bb1bac0b9cc45ea68ec44ccfec379a63c95182ea24a202ad1515f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__066d1cb5108ca43617ddb910f8c2877810b22dd9df69ca2808c0f2f0e5d3aa2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dryRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUtilization")
    def max_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUtilization"))

    @max_utilization.setter
    def max_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4f524b3d11f538d2341a0c460c487e5a37cf8523fe47f3c001aedafcf8dfb0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633c143a2edd46be950cee2729852a89ed29751307099021f2e8c880808639a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceBackendCustomMetrics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceBackendCustomMetrics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceBackendCustomMetrics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b4bc3750e962831b127285baeb37eb67b606f60e95ea9bfbb73fdfa4195c14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendServiceBackendList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceBackendList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0f1889fb0fb24811da4e8f71a34e59ae92cbe448d2540403bcc0638491aeabc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeBackendServiceBackendOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8817346a79c3d97c01b769a13ec90fdff2d8c390eba299c5de7d112140b55bd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeBackendServiceBackendOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d6ef3ff4b618d9253593a3de522ca28f5d53a23f49238a9552aca13e83ac6be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__196dc0bc639b1cc46f99345f318a3db744656a2e4b04b13ff2abc9fe3b60af49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28e9b3dd22df6082afb15c1087bfa33d2ed75702f42d592d6fd8a80e770d671c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceBackend]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceBackend]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceBackend]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__704d1395eaebe064b4082b10cebaa1de7eb5ad7acea921dfaed612f56c295042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendServiceBackendOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceBackendOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e257b59166910e01f59db784213cb24af01d5a7656335186a5a2266d210d958)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomMetrics")
    def put_custom_metrics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceBackendCustomMetrics, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604ea3a491b0b911e5bd00437a751a561e17d0812ed4721e43db2bd811435926)
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
    def custom_metrics(self) -> ComputeBackendServiceBackendCustomMetricsList:
        return typing.cast(ComputeBackendServiceBackendCustomMetricsList, jsii.get(self, "customMetrics"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceBackendCustomMetrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceBackendCustomMetrics]]], jsii.get(self, "customMetricsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7d2516a4d14ba70a207c45a0513800e2b3422af8233acfaaa292e5c5f871860e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "balancingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capacityScaler")
    def capacity_scaler(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "capacityScaler"))

    @capacity_scaler.setter
    def capacity_scaler(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6ddc1d98465231a397310c6dd7201eec6fc696341b760aa843247d4c906fc64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityScaler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__623c8f1ef6e81db622c7d77dd6f9fe4dc1b7f32b6ef9b2a67b6321e32e71c4f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__877d6ba72963eca51edaae733246f0ecb7712f45d3cd55e448bb7f7c5161399e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConnections")
    def max_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnections"))

    @max_connections.setter
    def max_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d1816f5475d20b492516570a55ff5254324360f12b8477c2fdcc2dd6d66b68e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConnectionsPerEndpoint")
    def max_connections_per_endpoint(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionsPerEndpoint"))

    @max_connections_per_endpoint.setter
    def max_connections_per_endpoint(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39deb44524038f3dc9f1dc6e1f11531de2c5a5d4d0953af0c317051b001818ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionsPerEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConnectionsPerInstance")
    def max_connections_per_instance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionsPerInstance"))

    @max_connections_per_instance.setter
    def max_connections_per_instance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c5702137305f5f9e4b15de1b1e9dc5dcf9676dc20ab9cc62dd8bef63b037703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionsPerInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRate")
    def max_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRate"))

    @max_rate.setter
    def max_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__638c60ea27b2a232dade2c0bc746d8b338985650df52007540039263cc91f44e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRatePerEndpoint")
    def max_rate_per_endpoint(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRatePerEndpoint"))

    @max_rate_per_endpoint.setter
    def max_rate_per_endpoint(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df371e4ebf3da50a4ecbb3817a68cd6f9253b7ccaaf5478fe01267c4b14224e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRatePerEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRatePerInstance")
    def max_rate_per_instance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRatePerInstance"))

    @max_rate_per_instance.setter
    def max_rate_per_instance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0af28b4cff5d6afa26211453ed869914da7bb2f0a17a5a1313c8dd2f97e07e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRatePerInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUtilization")
    def max_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUtilization"))

    @max_utilization.setter
    def max_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78ed33132efcad8ff0b50bc9b05c794b81328ef510d586e515fa46e20cf1d57a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preference")
    def preference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preference"))

    @preference.setter
    def preference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b5debb665558e57788d261a1f03eb2c983b86e3e8273f3f342728ee476bb576)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceBackend]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceBackend]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceBackend]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d945141484f0e78ab3bb08b7beab5069009f63aa5c513451cbc1957354f015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceCdnPolicy",
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
class ComputeBackendServiceCdnPolicy:
    def __init__(
        self,
        *,
        bypass_cache_on_request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cache_key_policy: typing.Optional[typing.Union["ComputeBackendServiceCdnPolicyCacheKeyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_mode: typing.Optional[builtins.str] = None,
        client_ttl: typing.Optional[jsii.Number] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        max_ttl: typing.Optional[jsii.Number] = None,
        negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negative_caching_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceCdnPolicyNegativeCachingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_coalescing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        serve_while_stale: typing.Optional[jsii.Number] = None,
        signed_url_cache_max_age_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bypass_cache_on_request_headers: bypass_cache_on_request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#bypass_cache_on_request_headers ComputeBackendService#bypass_cache_on_request_headers}
        :param cache_key_policy: cache_key_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#cache_key_policy ComputeBackendService#cache_key_policy}
        :param cache_mode: Specifies the cache setting for all responses from this backend. The possible values are: USE_ORIGIN_HEADERS, FORCE_CACHE_ALL and CACHE_ALL_STATIC Possible values: ["USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "CACHE_ALL_STATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#cache_mode ComputeBackendService#cache_mode}
        :param client_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#client_ttl ComputeBackendService#client_ttl}
        :param default_ttl: Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#default_ttl ComputeBackendService#default_ttl}
        :param max_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_ttl ComputeBackendService#max_ttl}
        :param negative_caching: Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#negative_caching ComputeBackendService#negative_caching}
        :param negative_caching_policy: negative_caching_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#negative_caching_policy ComputeBackendService#negative_caching_policy}
        :param request_coalescing: If true then Cloud CDN will combine multiple concurrent cache fill requests into a small number of requests to the origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#request_coalescing ComputeBackendService#request_coalescing}
        :param serve_while_stale: Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#serve_while_stale ComputeBackendService#serve_while_stale}
        :param signed_url_cache_max_age_sec: Maximum number of seconds the response to a signed URL request will be considered fresh, defaults to 1hr (3600s). After this time period, the response will be revalidated before being served. When serving responses to signed URL requests, Cloud CDN will internally behave as though all responses from this backend had a "Cache-Control: public, max-age=[TTL]" header, regardless of any existing Cache-Control header. The actual headers served in responses will not be altered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#signed_url_cache_max_age_sec ComputeBackendService#signed_url_cache_max_age_sec}
        '''
        if isinstance(cache_key_policy, dict):
            cache_key_policy = ComputeBackendServiceCdnPolicyCacheKeyPolicy(**cache_key_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4aa11413bfd687862b953cafd3548ecf6de4848d4c2b7181b0c3db1af6de753)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders"]]]:
        '''bypass_cache_on_request_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#bypass_cache_on_request_headers ComputeBackendService#bypass_cache_on_request_headers}
        '''
        result = self._values.get("bypass_cache_on_request_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders"]]], result)

    @builtins.property
    def cache_key_policy(
        self,
    ) -> typing.Optional["ComputeBackendServiceCdnPolicyCacheKeyPolicy"]:
        '''cache_key_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#cache_key_policy ComputeBackendService#cache_key_policy}
        '''
        result = self._values.get("cache_key_policy")
        return typing.cast(typing.Optional["ComputeBackendServiceCdnPolicyCacheKeyPolicy"], result)

    @builtins.property
    def cache_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the cache setting for all responses from this backend.

        The possible values are: USE_ORIGIN_HEADERS, FORCE_CACHE_ALL and CACHE_ALL_STATIC Possible values: ["USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "CACHE_ALL_STATIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#cache_mode ComputeBackendService#cache_mode}
        '''
        result = self._values.get("cache_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_ttl(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum allowed TTL for cached content served by this origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#client_ttl ComputeBackendService#client_ttl}
        '''
        result = self._values.get("client_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_ttl(self) -> typing.Optional[jsii.Number]:
        '''Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#default_ttl ComputeBackendService#default_ttl}
        '''
        result = self._values.get("default_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_ttl(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum allowed TTL for cached content served by this origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_ttl ComputeBackendService#max_ttl}
        '''
        result = self._values.get("max_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def negative_caching(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#negative_caching ComputeBackendService#negative_caching}
        '''
        result = self._values.get("negative_caching")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def negative_caching_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceCdnPolicyNegativeCachingPolicy"]]]:
        '''negative_caching_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#negative_caching_policy ComputeBackendService#negative_caching_policy}
        '''
        result = self._values.get("negative_caching_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceCdnPolicyNegativeCachingPolicy"]]], result)

    @builtins.property
    def request_coalescing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true then Cloud CDN will combine multiple concurrent cache fill requests into a small number of requests to the origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#request_coalescing ComputeBackendService#request_coalescing}
        '''
        result = self._values.get("request_coalescing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def serve_while_stale(self) -> typing.Optional[jsii.Number]:
        '''Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#serve_while_stale ComputeBackendService#serve_while_stale}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#signed_url_cache_max_age_sec ComputeBackendService#signed_url_cache_max_age_sec}
        '''
        result = self._values.get("signed_url_cache_max_age_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceCdnPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName"},
)
class ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders:
    def __init__(self, *, header_name: builtins.str) -> None:
        '''
        :param header_name: The header field name to match on when bypassing cache. Values are case-insensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#header_name ComputeBackendService#header_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d635107e864305f2ec286c8bafef183b5522d8ac838af18d9ff0a76c38c97f)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
        }

    @builtins.property
    def header_name(self) -> builtins.str:
        '''The header field name to match on when bypassing cache. Values are case-insensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#header_name ComputeBackendService#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e43a19bafcdb974380abc4367a5f610e98a5063ff689211c895760ef2253abc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb6d033c7291d0bb7e526d5daa98010f42ff8925f0a476c99e99ebccb25a9dd4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ca499ebf4a52baf2d75eb73d54ce71abd6cd2a48a284469e89025699f5b0cb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__015289f9133af29e10da36474dd3b775a9a727ec0307ec84a80f271fef9a7fe0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fb2ca296e183cc02029ccc8c9aa1590967e6a7df3fa4f40801fb344c1c40ef3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f36b151cc4336707ae4b413751d9bf5a1d7e8c2997e02a31e6fb70a2494ad6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cb008bcb1a6622a0d601cee5ce5496f35a4a8ec23bc7f2205f7af011d978eae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e7e0430c10110afc99b017097dfae38de9b93fbc629a39f692afbc7385118f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28fe2b9869e13ebea594a0ec2ebf500ed98ab5f2b43c8af004c69482e0f8744b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceCdnPolicyCacheKeyPolicy",
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
class ComputeBackendServiceCdnPolicyCacheKeyPolicy:
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
        :param include_host: If true requests to different hosts will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#include_host ComputeBackendService#include_host}
        :param include_http_headers: Allows HTTP request headers (by name) to be used in the cache key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#include_http_headers ComputeBackendService#include_http_headers}
        :param include_named_cookies: Names of cookies to include in cache keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#include_named_cookies ComputeBackendService#include_named_cookies}
        :param include_protocol: If true, http and https requests will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#include_protocol ComputeBackendService#include_protocol}
        :param include_query_string: If true, include query string parameters in the cache key according to query_string_whitelist and query_string_blacklist. If neither is set, the entire query string will be included. If false, the query string will be excluded from the cache key entirely. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#include_query_string ComputeBackendService#include_query_string}
        :param query_string_blacklist: Names of query string parameters to exclude in cache keys. All other parameters will be included. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#query_string_blacklist ComputeBackendService#query_string_blacklist}
        :param query_string_whitelist: Names of query string parameters to include in cache keys. All other parameters will be excluded. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#query_string_whitelist ComputeBackendService#query_string_whitelist}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e4b8e187644f2dc323781f3443cd1ef24e4767b558ed8df84498f3b0862e8ae)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#include_host ComputeBackendService#include_host}
        '''
        result = self._values.get("include_host")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_http_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Allows HTTP request headers (by name) to be used in the cache key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#include_http_headers ComputeBackendService#include_http_headers}
        '''
        result = self._values.get("include_http_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_named_cookies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of cookies to include in cache keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#include_named_cookies ComputeBackendService#include_named_cookies}
        '''
        result = self._values.get("include_named_cookies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, http and https requests will be cached separately.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#include_protocol ComputeBackendService#include_protocol}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#include_query_string ComputeBackendService#include_query_string}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#query_string_blacklist ComputeBackendService#query_string_blacklist}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#query_string_whitelist ComputeBackendService#query_string_whitelist}
        '''
        result = self._values.get("query_string_whitelist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceCdnPolicyCacheKeyPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceCdnPolicyCacheKeyPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceCdnPolicyCacheKeyPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd217cc1b9015265b5f02b01a5167bc5bdcd21d3d541acb095d4976515b8e145)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ed81a436bb763aab5d10ef41dbf6b250f40648e6ce535381069049fb1f5d92a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeHttpHeaders")
    def include_http_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeHttpHeaders"))

    @include_http_headers.setter
    def include_http_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d73664ee1221c25d5829c5028b00a367e106c81e2a9aea1cad9650394f42d0a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeHttpHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeNamedCookies")
    def include_named_cookies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeNamedCookies"))

    @include_named_cookies.setter
    def include_named_cookies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d69d764bc36e5aec06110dade800e05823238f54ecfaa51832fd80494a0b0ab3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8b10dbd15eefa6ffa55c77499b8587bc826ffd273fccc87a9be783fe867361d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff38362765670cf0b4d96792c32207570c072e4030e74cdce09565b8448bf2f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeQueryString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringBlacklist")
    def query_string_blacklist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryStringBlacklist"))

    @query_string_blacklist.setter
    def query_string_blacklist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b5221d51574d6d6dbd77b81793c6efb3a34f0e6ba4d70e041af205540d0d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringBlacklist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringWhitelist")
    def query_string_whitelist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryStringWhitelist"))

    @query_string_whitelist.setter
    def query_string_whitelist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f48d994fefd0f29ba6ea30930decb8cc268448b1e973a7426fd268bcdf97ad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringWhitelist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeBackendServiceCdnPolicyCacheKeyPolicy]:
        return typing.cast(typing.Optional[ComputeBackendServiceCdnPolicyCacheKeyPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceCdnPolicyCacheKeyPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0a6e377ab94f4fd6dfa738e7909fdd95912ac0d431f167639fcfa769d55159e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceCdnPolicyNegativeCachingPolicy",
    jsii_struct_bases=[],
    name_mapping={"code": "code", "ttl": "ttl"},
)
class ComputeBackendServiceCdnPolicyNegativeCachingPolicy:
    def __init__(
        self,
        *,
        code: typing.Optional[jsii.Number] = None,
        ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param code: The HTTP status code to define a TTL against. Only HTTP status codes 300, 301, 308, 404, 405, 410, 421, 451 and 501 can be specified as values, and you cannot specify a status code more than once. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#code ComputeBackendService#code}
        :param ttl: The TTL (in seconds) for which to cache responses with the corresponding status code. The maximum allowed value is 1800s (30 minutes), noting that infrequently accessed objects may be evicted from the cache before the defined TTL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#ttl ComputeBackendService#ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e75de7edcfabb1463e16c83bd3d248dc59b1982fba0d598463dd35be8721193)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#code ComputeBackendService#code}
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''The TTL (in seconds) for which to cache responses with the corresponding status code.

        The maximum allowed value is 1800s
        (30 minutes), noting that infrequently accessed objects may be evicted from the cache before the defined TTL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#ttl ComputeBackendService#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceCdnPolicyNegativeCachingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceCdnPolicyNegativeCachingPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceCdnPolicyNegativeCachingPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7468b40278131f5eceb36f1547ede5cb4d93ab8196d66df2012971eb77f4d720)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeBackendServiceCdnPolicyNegativeCachingPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e5dbcfe7d8efda15f2c3387d9cc5c936d1b1dd47a0b76160f5a16bf5df22b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeBackendServiceCdnPolicyNegativeCachingPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ae33597bfad4df6300de5bbb616a28959e30efba6566ccaa0363d5c6ce8b15f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e95b76d5c8c8f6bd0ae52c9a0269bb648b9883944d55ac4292128fbb3625b131)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac3ad171e897745a023d9e4bcb3647ac1567375dfdbc4c83ae005ee3fbc09134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCdnPolicyNegativeCachingPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCdnPolicyNegativeCachingPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCdnPolicyNegativeCachingPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f40a26c44b5253b4c56057aaca3ad6e09d7a42c0c62c91f66afdcccd303cb7ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendServiceCdnPolicyNegativeCachingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceCdnPolicyNegativeCachingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91f106b62dc4b14cae11d76079a491a2905b0159bd8a45bace3e3503cffdf496)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32093ae86b56641b7f9b3035ce5e91f2938647a1344c62a2e4a12ca4ebeb844e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee3961a7fc2834fae134d66cdb74b302e850e24f5f9f998dbaeff3ada189008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceCdnPolicyNegativeCachingPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceCdnPolicyNegativeCachingPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceCdnPolicyNegativeCachingPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961a41302b70499e5465c85b982a832150b19c6c3fc8eca5af9c68eef0c9579c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendServiceCdnPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceCdnPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13b0b2e545804d6abb22357379cae31ed3769d64911f7781dcc58237e18fce0c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBypassCacheOnRequestHeaders")
    def put_bypass_cache_on_request_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d327e2eac71b95b8971702bd79146a9582c730cf2f76afc1de5ef46b166cb0b)
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
        :param include_host: If true requests to different hosts will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#include_host ComputeBackendService#include_host}
        :param include_http_headers: Allows HTTP request headers (by name) to be used in the cache key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#include_http_headers ComputeBackendService#include_http_headers}
        :param include_named_cookies: Names of cookies to include in cache keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#include_named_cookies ComputeBackendService#include_named_cookies}
        :param include_protocol: If true, http and https requests will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#include_protocol ComputeBackendService#include_protocol}
        :param include_query_string: If true, include query string parameters in the cache key according to query_string_whitelist and query_string_blacklist. If neither is set, the entire query string will be included. If false, the query string will be excluded from the cache key entirely. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#include_query_string ComputeBackendService#include_query_string}
        :param query_string_blacklist: Names of query string parameters to exclude in cache keys. All other parameters will be included. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#query_string_blacklist ComputeBackendService#query_string_blacklist}
        :param query_string_whitelist: Names of query string parameters to include in cache keys. All other parameters will be excluded. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#query_string_whitelist ComputeBackendService#query_string_whitelist}
        '''
        value = ComputeBackendServiceCdnPolicyCacheKeyPolicy(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceCdnPolicyNegativeCachingPolicy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762feef19670ce9239d545e3c3e8d13399966ce5122ac9c312a609cb3b30f394)
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
    ) -> ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersList:
        return typing.cast(ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersList, jsii.get(self, "bypassCacheOnRequestHeaders"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyPolicy")
    def cache_key_policy(
        self,
    ) -> ComputeBackendServiceCdnPolicyCacheKeyPolicyOutputReference:
        return typing.cast(ComputeBackendServiceCdnPolicyCacheKeyPolicyOutputReference, jsii.get(self, "cacheKeyPolicy"))

    @builtins.property
    @jsii.member(jsii_name="negativeCachingPolicy")
    def negative_caching_policy(
        self,
    ) -> ComputeBackendServiceCdnPolicyNegativeCachingPolicyList:
        return typing.cast(ComputeBackendServiceCdnPolicyNegativeCachingPolicyList, jsii.get(self, "negativeCachingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="bypassCacheOnRequestHeadersInput")
    def bypass_cache_on_request_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]]], jsii.get(self, "bypassCacheOnRequestHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyPolicyInput")
    def cache_key_policy_input(
        self,
    ) -> typing.Optional[ComputeBackendServiceCdnPolicyCacheKeyPolicy]:
        return typing.cast(typing.Optional[ComputeBackendServiceCdnPolicyCacheKeyPolicy], jsii.get(self, "cacheKeyPolicyInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCdnPolicyNegativeCachingPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCdnPolicyNegativeCachingPolicy]]], jsii.get(self, "negativeCachingPolicyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3ac16ac0af5022071fbe022094565931b2903aeeb88330294962424efcf99dde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTtl")
    def client_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientTtl"))

    @client_ttl.setter
    def client_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8671ae97b71554ef457e726ac4770ec63a27c9a724235ba76a9649c0fb1606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eb811b573498d4705c4d804bd3b545a031df2fc26984c5d6824cf36cdefd60d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTtl")
    def max_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxTtl"))

    @max_ttl.setter
    def max_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e017bc59c556a2f13f4f44350f919e2d123d47451ab638504a3c4d0152af7f25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__417e062007cbf6d45935cd042e7c3c971a6b0dc3311ba72b647e2eba6b7aba4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d97c35b6cc6d794e29b95c0f954a1b5a48b026d2b67671301ab68cc5b4e2aca7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestCoalescing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serveWhileStale")
    def serve_while_stale(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "serveWhileStale"))

    @serve_while_stale.setter
    def serve_while_stale(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d7212cca2bec89b9d39cdb9324eaaa4ac3a04e0c5f84c4066892d7391a05ebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serveWhileStale", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signedUrlCacheMaxAgeSec")
    def signed_url_cache_max_age_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "signedUrlCacheMaxAgeSec"))

    @signed_url_cache_max_age_sec.setter
    def signed_url_cache_max_age_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb995bbea02eda253769b8533cc37492371c20b35eca24012b750e5f633335a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signedUrlCacheMaxAgeSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeBackendServiceCdnPolicy]:
        return typing.cast(typing.Optional[ComputeBackendServiceCdnPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceCdnPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493125191f9c980a5540244693e0987f4c01a24133cddf4dc00cfff1027faa3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceCircuitBreakers",
    jsii_struct_bases=[],
    name_mapping={
        "max_connections": "maxConnections",
        "max_pending_requests": "maxPendingRequests",
        "max_requests": "maxRequests",
        "max_requests_per_connection": "maxRequestsPerConnection",
        "max_retries": "maxRetries",
    },
)
class ComputeBackendServiceCircuitBreakers:
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
        :param max_connections: The maximum number of connections to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_connections ComputeBackendService#max_connections}
        :param max_pending_requests: The maximum number of pending requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_pending_requests ComputeBackendService#max_pending_requests}
        :param max_requests: The maximum number of parallel requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_requests ComputeBackendService#max_requests}
        :param max_requests_per_connection: Maximum requests for a single backend connection. This parameter is respected by both the HTTP/1.1 and HTTP/2 implementations. If not specified, there is no limit. Setting this parameter to 1 will effectively disable keep alive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_requests_per_connection ComputeBackendService#max_requests_per_connection}
        :param max_retries: The maximum number of parallel retries to the backend cluster. Defaults to 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_retries ComputeBackendService#max_retries}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cabb5dd50ebcf417ca6d890e8eabad68602526db561901f7904f994168fe8b2f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_connections ComputeBackendService#max_connections}
        '''
        result = self._values.get("max_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_pending_requests(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of pending requests to the backend cluster. Defaults to 1024.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_pending_requests ComputeBackendService#max_pending_requests}
        '''
        result = self._values.get("max_pending_requests")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_requests(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of parallel requests to the backend cluster. Defaults to 1024.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_requests ComputeBackendService#max_requests}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_requests_per_connection ComputeBackendService#max_requests_per_connection}
        '''
        result = self._values.get("max_requests_per_connection")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of parallel retries to the backend cluster. Defaults to 3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_retries ComputeBackendService#max_retries}
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceCircuitBreakers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceCircuitBreakersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceCircuitBreakersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e1f4aadcbd8d97c0ae65c4ae65f1f6a5a3cc16749d2c4c1eeb4948118ac5d62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db1a9dc1a125e18fa78b09da195dfbcb8108bf90c518568c70c2ba06032a1101)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPendingRequests")
    def max_pending_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPendingRequests"))

    @max_pending_requests.setter
    def max_pending_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046c38d353eb17c495b3615bab450e7a5e6e7f984310a32d396fd789ffd0923d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPendingRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRequests")
    def max_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRequests"))

    @max_requests.setter
    def max_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d003517abd224c1aa133a618eda57fcb5ca7fd287b43598afc3ad1b6d63f3e61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRequestsPerConnection")
    def max_requests_per_connection(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRequestsPerConnection"))

    @max_requests_per_connection.setter
    def max_requests_per_connection(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2f102e717387f1df42d2235cebdf1a7a16ec13aafbd43c7e2e6f42c7e7fefd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRequestsPerConnection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa95b5e7795cc254ad79205ff211bb4f7454c756e1656edcacc178c2c5f8257)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeBackendServiceCircuitBreakers]:
        return typing.cast(typing.Optional[ComputeBackendServiceCircuitBreakers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceCircuitBreakers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e6e0dccbc322916e5e2fe1426b9a099501fa355739dc0e62be5c2ced20855f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceConfig",
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
class ComputeBackendServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cdn_policy: typing.Optional[typing.Union[ComputeBackendServiceCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        circuit_breakers: typing.Optional[typing.Union[ComputeBackendServiceCircuitBreakers, typing.Dict[builtins.str, typing.Any]]] = None,
        compression_mode: typing.Optional[builtins.str] = None,
        connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
        consistent_hash: typing.Optional[typing.Union["ComputeBackendServiceConsistentHash", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceCustomMetrics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_request_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_response_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        edge_security_policy: typing.Optional[builtins.str] = None,
        enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_managed_migration_state: typing.Optional[builtins.str] = None,
        external_managed_migration_testing_percentage: typing.Optional[jsii.Number] = None,
        health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        iap: typing.Optional[typing.Union["ComputeBackendServiceIap", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address_selection_policy: typing.Optional[builtins.str] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        locality_lb_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceLocalityLbPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        locality_lb_policy: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["ComputeBackendServiceLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        max_stream_duration: typing.Optional[typing.Union["ComputeBackendServiceMaxStreamDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        outlier_detection: typing.Optional[typing.Union["ComputeBackendServiceOutlierDetection", typing.Dict[builtins.str, typing.Any]]] = None,
        port_name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        security_policy: typing.Optional[builtins.str] = None,
        security_settings: typing.Optional[typing.Union["ComputeBackendServiceSecuritySettings", typing.Dict[builtins.str, typing.Any]]] = None,
        service_lb_policy: typing.Optional[builtins.str] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        strong_session_affinity_cookie: typing.Optional[typing.Union["ComputeBackendServiceStrongSessionAffinityCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeBackendServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_sec: typing.Optional[jsii.Number] = None,
        tls_settings: typing.Optional[typing.Union["ComputeBackendServiceTlsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        :param affinity_cookie_ttl_sec: Lifetime of cookies in seconds if session_affinity is GENERATED_COOKIE. If set to 0, the cookie is non-persistent and lasts only until the end of the browser session (or equivalent). The maximum allowed value for TTL is one day. When the load balancing scheme is INTERNAL, this field is not used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#affinity_cookie_ttl_sec ComputeBackendService#affinity_cookie_ttl_sec}
        :param backend: backend block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#backend ComputeBackendService#backend}
        :param cdn_policy: cdn_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#cdn_policy ComputeBackendService#cdn_policy}
        :param circuit_breakers: circuit_breakers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#circuit_breakers ComputeBackendService#circuit_breakers}
        :param compression_mode: Compress text responses using Brotli or gzip compression, based on the client's Accept-Encoding header. Possible values: ["AUTOMATIC", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#compression_mode ComputeBackendService#compression_mode}
        :param connection_draining_timeout_sec: Time for which instance will be drained (not accept new connections, but still work to finish started). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#connection_draining_timeout_sec ComputeBackendService#connection_draining_timeout_sec}
        :param consistent_hash: consistent_hash block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#consistent_hash ComputeBackendService#consistent_hash}
        :param custom_metrics: custom_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#custom_metrics ComputeBackendService#custom_metrics}
        :param custom_request_headers: Headers that the HTTP/S load balancer should add to proxied requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#custom_request_headers ComputeBackendService#custom_request_headers}
        :param custom_response_headers: Headers that the HTTP/S load balancer should add to proxied responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#custom_response_headers ComputeBackendService#custom_response_headers}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#description ComputeBackendService#description}
        :param edge_security_policy: The resource URL for the edge security policy associated with this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#edge_security_policy ComputeBackendService#edge_security_policy}
        :param enable_cdn: If true, enable Cloud CDN for this BackendService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enable_cdn ComputeBackendService#enable_cdn}
        :param external_managed_migration_state: Specifies the canary migration state. Possible values are PREPARE, TEST_BY_PERCENTAGE, and TEST_ALL_TRAFFIC. To begin the migration from EXTERNAL to EXTERNAL_MANAGED, the state must be changed to PREPARE. The state must be changed to TEST_ALL_TRAFFIC before the loadBalancingScheme can be changed to EXTERNAL_MANAGED. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate traffic by percentage using externalManagedMigrationTestingPercentage. Rolling back a migration requires the states to be set in reverse order. So changing the scheme from EXTERNAL_MANAGED to EXTERNAL requires the state to be set to TEST_ALL_TRAFFIC at the same time. Optionally, the TEST_BY_PERCENTAGE state can be used to migrate some traffic back to EXTERNAL or PREPARE can be used to migrate all traffic back to EXTERNAL. Possible values: ["PREPARE", "TEST_BY_PERCENTAGE", "TEST_ALL_TRAFFIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#external_managed_migration_state ComputeBackendService#external_managed_migration_state}
        :param external_managed_migration_testing_percentage: Determines the fraction of requests that should be processed by the Global external Application Load Balancer. The value of this field must be in the range [0, 100]. Session affinity options will slightly affect this routing behavior, for more details, see: Session Affinity. This value can only be set if the loadBalancingScheme in the backend service is set to EXTERNAL (when using the Classic ALB) and the migration state is TEST_BY_PERCENTAGE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#external_managed_migration_testing_percentage ComputeBackendService#external_managed_migration_testing_percentage}
        :param health_checks: The set of URLs to the HttpHealthCheck or HttpsHealthCheck resource for health checking this BackendService. Currently at most one health check can be specified. A health check must be specified unless the backend service uses an internet or serverless NEG as a backend. For internal load balancing, a URL to a HealthCheck resource must be specified instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#health_checks ComputeBackendService#health_checks}
        :param iap: iap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#iap ComputeBackendService#iap}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#id ComputeBackendService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address_selection_policy: Specifies preference of traffic to the backend (from the proxy and from the client for proxyless gRPC). Possible values: ["IPV4_ONLY", "PREFER_IPV6", "IPV6_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#ip_address_selection_policy ComputeBackendService#ip_address_selection_policy}
        :param load_balancing_scheme: Indicates whether the backend service will be used with internal or external load balancing. A backend service created for one type of load balancing cannot be used with the other. For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "INTERNAL_SELF_MANAGED", "INTERNAL_MANAGED", "EXTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#load_balancing_scheme ComputeBackendService#load_balancing_scheme}
        :param locality_lb_policies: locality_lb_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#locality_lb_policies ComputeBackendService#locality_lb_policies}
        :param locality_lb_policy: The load balancing algorithm used within the scope of the locality. The possible values are:. - 'ROUND_ROBIN': This is a simple policy in which each healthy backend is selected in round robin order. - 'LEAST_REQUEST': An O(1) algorithm which selects two random healthy hosts and picks the host which has fewer active requests. - 'RING_HASH': The ring/modulo hash load balancer implements consistent hashing to backends. The algorithm has the property that the addition/removal of a host from a set of N hosts only affects 1/N of the requests. - 'RANDOM': The load balancer selects a random healthy host. - 'ORIGINAL_DESTINATION': Backend host is selected based on the client connection metadata, i.e., connections are opened to the same address as the destination address of the incoming connection before the connection was redirected to the load balancer. - 'MAGLEV': used as a drop in replacement for the ring hash load balancer. Maglev is not as stable as ring hash but has faster table lookup build times and host selection times. For more information about Maglev, refer to https://ai.google/research/pubs/pub44824 - 'WEIGHTED_MAGLEV': Per-instance weighted Load Balancing via health check reported weights. Only applicable to loadBalancingScheme EXTERNAL. If set, the Backend Service must configure a non legacy HTTP-based Health Check, and health check replies are expected to contain non-standard HTTP response header field X-Load-Balancing-Endpoint-Weight to specify the per-instance weights. If set, Load Balancing is weight based on the per-instance weights reported in the last processed health check replies, as long as every instance either reported a valid weight or had UNAVAILABLE_WEIGHT. Otherwise, Load Balancing remains equal-weight. - 'WEIGHTED_ROUND_ROBIN': Per-endpoint weighted round-robin Load Balancing using weights computed from Backend reported Custom Metrics. If set, the Backend Service responses are expected to contain non-standard HTTP response header field X-Endpoint-Load-Metrics. The reported metrics to use for computing the weights are specified via the backends[].customMetrics fields. locality_lb_policy is applicable to either: - A regional backend service with the service_protocol set to HTTP, HTTPS, HTTP2 or H2C, and loadBalancingScheme set to INTERNAL_MANAGED. - A global backend service with the load_balancing_scheme set to INTERNAL_SELF_MANAGED. - A regional backend service with loadBalancingScheme set to EXTERNAL (External Network Load Balancing). Only MAGLEV and WEIGHTED_MAGLEV values are possible for External Network Load Balancing. The default is MAGLEV. If session_affinity is not NONE, and locality_lb_policy is not set to MAGLEV, WEIGHTED_MAGLEV, or RING_HASH, session affinity settings will not take effect. Only ROUND_ROBIN and RING_HASH are supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validate_for_proxyless field set to true. Possible values: ["ROUND_ROBIN", "LEAST_REQUEST", "RING_HASH", "RANDOM", "ORIGINAL_DESTINATION", "MAGLEV", "WEIGHTED_MAGLEV", "WEIGHTED_ROUND_ROBIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#locality_lb_policy ComputeBackendService#locality_lb_policy}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#log_config ComputeBackendService#log_config}
        :param max_stream_duration: max_stream_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_stream_duration ComputeBackendService#max_stream_duration}
        :param outlier_detection: outlier_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#outlier_detection ComputeBackendService#outlier_detection}
        :param port_name: Name of backend port. The same name should appear in the instance groups referenced by this service. Required when the load balancing scheme is EXTERNAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#port_name ComputeBackendService#port_name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#project ComputeBackendService#project}.
        :param protocol: The protocol this BackendService uses to communicate with backends. The default is HTTP. Possible values are HTTP, HTTPS, HTTP2, H2C, TCP, SSL, UDP or GRPC. Refer to the documentation for the load balancers or for Traffic Director for more information. Must be set to GRPC when the backend service is referenced by a URL map that is bound to target gRPC proxy. Possible values: ["HTTP", "HTTPS", "HTTP2", "TCP", "SSL", "UDP", "GRPC", "UNSPECIFIED", "H2C"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#protocol ComputeBackendService#protocol}
        :param security_policy: The security policy associated with this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#security_policy ComputeBackendService#security_policy}
        :param security_settings: security_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#security_settings ComputeBackendService#security_settings}
        :param service_lb_policy: URL to networkservices.ServiceLbPolicy resource. Can only be set if load balancing scheme is EXTERNAL, EXTERNAL_MANAGED, INTERNAL_MANAGED or INTERNAL_SELF_MANAGED and the scope is global. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#service_lb_policy ComputeBackendService#service_lb_policy}
        :param session_affinity: Type of session affinity to use. The default is NONE. Session affinity is not applicable if the protocol is UDP. Possible values: ["NONE", "CLIENT_IP", "CLIENT_IP_PORT_PROTO", "CLIENT_IP_PROTO", "GENERATED_COOKIE", "HEADER_FIELD", "HTTP_COOKIE", "STRONG_COOKIE_AFFINITY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#session_affinity ComputeBackendService#session_affinity}
        :param strong_session_affinity_cookie: strong_session_affinity_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#strong_session_affinity_cookie ComputeBackendService#strong_session_affinity_cookie}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#timeouts ComputeBackendService#timeouts}
        :param timeout_sec: The backend service timeout has a different meaning depending on the type of load balancer. For more information see, `Backend service settings <https://cloud.google.com/compute/docs/reference/rest/v1/backendServices>`_. The default is 30 seconds. The full range of timeout values allowed goes from 1 through 2,147,483,647 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#timeout_sec ComputeBackendService#timeout_sec}
        :param tls_settings: tls_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#tls_settings ComputeBackendService#tls_settings}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cdn_policy, dict):
            cdn_policy = ComputeBackendServiceCdnPolicy(**cdn_policy)
        if isinstance(circuit_breakers, dict):
            circuit_breakers = ComputeBackendServiceCircuitBreakers(**circuit_breakers)
        if isinstance(consistent_hash, dict):
            consistent_hash = ComputeBackendServiceConsistentHash(**consistent_hash)
        if isinstance(iap, dict):
            iap = ComputeBackendServiceIap(**iap)
        if isinstance(log_config, dict):
            log_config = ComputeBackendServiceLogConfig(**log_config)
        if isinstance(max_stream_duration, dict):
            max_stream_duration = ComputeBackendServiceMaxStreamDuration(**max_stream_duration)
        if isinstance(outlier_detection, dict):
            outlier_detection = ComputeBackendServiceOutlierDetection(**outlier_detection)
        if isinstance(security_settings, dict):
            security_settings = ComputeBackendServiceSecuritySettings(**security_settings)
        if isinstance(strong_session_affinity_cookie, dict):
            strong_session_affinity_cookie = ComputeBackendServiceStrongSessionAffinityCookie(**strong_session_affinity_cookie)
        if isinstance(timeouts, dict):
            timeouts = ComputeBackendServiceTimeouts(**timeouts)
        if isinstance(tls_settings, dict):
            tls_settings = ComputeBackendServiceTlsSettings(**tls_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cdf2349083c2692c68d52e8aef7e24451d6ac647ece4b93819a2c462dedcbcc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#affinity_cookie_ttl_sec ComputeBackendService#affinity_cookie_ttl_sec}
        '''
        result = self._values.get("affinity_cookie_ttl_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def backend(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceBackend]]]:
        '''backend block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#backend ComputeBackendService#backend}
        '''
        result = self._values.get("backend")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceBackend]]], result)

    @builtins.property
    def cdn_policy(self) -> typing.Optional[ComputeBackendServiceCdnPolicy]:
        '''cdn_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#cdn_policy ComputeBackendService#cdn_policy}
        '''
        result = self._values.get("cdn_policy")
        return typing.cast(typing.Optional[ComputeBackendServiceCdnPolicy], result)

    @builtins.property
    def circuit_breakers(self) -> typing.Optional[ComputeBackendServiceCircuitBreakers]:
        '''circuit_breakers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#circuit_breakers ComputeBackendService#circuit_breakers}
        '''
        result = self._values.get("circuit_breakers")
        return typing.cast(typing.Optional[ComputeBackendServiceCircuitBreakers], result)

    @builtins.property
    def compression_mode(self) -> typing.Optional[builtins.str]:
        '''Compress text responses using Brotli or gzip compression, based on the client's Accept-Encoding header. Possible values: ["AUTOMATIC", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#compression_mode ComputeBackendService#compression_mode}
        '''
        result = self._values.get("compression_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_draining_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Time for which instance will be drained (not accept new connections, but still work to finish started).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#connection_draining_timeout_sec ComputeBackendService#connection_draining_timeout_sec}
        '''
        result = self._values.get("connection_draining_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def consistent_hash(self) -> typing.Optional["ComputeBackendServiceConsistentHash"]:
        '''consistent_hash block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#consistent_hash ComputeBackendService#consistent_hash}
        '''
        result = self._values.get("consistent_hash")
        return typing.cast(typing.Optional["ComputeBackendServiceConsistentHash"], result)

    @builtins.property
    def custom_metrics(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceCustomMetrics"]]]:
        '''custom_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#custom_metrics ComputeBackendService#custom_metrics}
        '''
        result = self._values.get("custom_metrics")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceCustomMetrics"]]], result)

    @builtins.property
    def custom_request_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Headers that the HTTP/S load balancer should add to proxied requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#custom_request_headers ComputeBackendService#custom_request_headers}
        '''
        result = self._values.get("custom_request_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def custom_response_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Headers that the HTTP/S load balancer should add to proxied responses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#custom_response_headers ComputeBackendService#custom_response_headers}
        '''
        result = self._values.get("custom_response_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#description ComputeBackendService#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_security_policy(self) -> typing.Optional[builtins.str]:
        '''The resource URL for the edge security policy associated with this backend service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#edge_security_policy ComputeBackendService#edge_security_policy}
        '''
        result = self._values.get("edge_security_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_cdn(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, enable Cloud CDN for this BackendService.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enable_cdn ComputeBackendService#enable_cdn}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#external_managed_migration_state ComputeBackendService#external_managed_migration_state}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#external_managed_migration_testing_percentage ComputeBackendService#external_managed_migration_testing_percentage}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#health_checks ComputeBackendService#health_checks}
        '''
        result = self._values.get("health_checks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def iap(self) -> typing.Optional["ComputeBackendServiceIap"]:
        '''iap block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#iap ComputeBackendService#iap}
        '''
        result = self._values.get("iap")
        return typing.cast(typing.Optional["ComputeBackendServiceIap"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#id ComputeBackendService#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address_selection_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies preference of traffic to the backend (from the proxy and from the client for proxyless gRPC).

        Possible values: ["IPV4_ONLY", "PREFER_IPV6", "IPV6_ONLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#ip_address_selection_policy ComputeBackendService#ip_address_selection_policy}
        '''
        result = self._values.get("ip_address_selection_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancing_scheme(self) -> typing.Optional[builtins.str]:
        '''Indicates whether the backend service will be used with internal or external load balancing.

        A backend service created for one type of
        load balancing cannot be used with the other. For more information, refer to
        `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_. Default value: "EXTERNAL" Possible values: ["EXTERNAL", "INTERNAL_SELF_MANAGED", "INTERNAL_MANAGED", "EXTERNAL_MANAGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#load_balancing_scheme ComputeBackendService#load_balancing_scheme}
        '''
        result = self._values.get("load_balancing_scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locality_lb_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceLocalityLbPolicies"]]]:
        '''locality_lb_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#locality_lb_policies ComputeBackendService#locality_lb_policies}
        '''
        result = self._values.get("locality_lb_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceLocalityLbPolicies"]]], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#locality_lb_policy ComputeBackendService#locality_lb_policy}
        '''
        result = self._values.get("locality_lb_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_config(self) -> typing.Optional["ComputeBackendServiceLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#log_config ComputeBackendService#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["ComputeBackendServiceLogConfig"], result)

    @builtins.property
    def max_stream_duration(
        self,
    ) -> typing.Optional["ComputeBackendServiceMaxStreamDuration"]:
        '''max_stream_duration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_stream_duration ComputeBackendService#max_stream_duration}
        '''
        result = self._values.get("max_stream_duration")
        return typing.cast(typing.Optional["ComputeBackendServiceMaxStreamDuration"], result)

    @builtins.property
    def outlier_detection(
        self,
    ) -> typing.Optional["ComputeBackendServiceOutlierDetection"]:
        '''outlier_detection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#outlier_detection ComputeBackendService#outlier_detection}
        '''
        result = self._values.get("outlier_detection")
        return typing.cast(typing.Optional["ComputeBackendServiceOutlierDetection"], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Name of backend port.

        The same name should appear in the instance
        groups referenced by this service. Required when the load balancing
        scheme is EXTERNAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#port_name ComputeBackendService#port_name}
        '''
        result = self._values.get("port_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#project ComputeBackendService#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol this BackendService uses to communicate with backends.

        The default is HTTP. Possible values are HTTP, HTTPS, HTTP2, H2C, TCP, SSL, UDP
        or GRPC. Refer to the documentation for the load balancers or for Traffic Director
        for more information. Must be set to GRPC when the backend service is referenced
        by a URL map that is bound to target gRPC proxy. Possible values: ["HTTP", "HTTPS", "HTTP2", "TCP", "SSL", "UDP", "GRPC", "UNSPECIFIED", "H2C"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#protocol ComputeBackendService#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_policy(self) -> typing.Optional[builtins.str]:
        '''The security policy associated with this backend service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#security_policy ComputeBackendService#security_policy}
        '''
        result = self._values.get("security_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_settings(
        self,
    ) -> typing.Optional["ComputeBackendServiceSecuritySettings"]:
        '''security_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#security_settings ComputeBackendService#security_settings}
        '''
        result = self._values.get("security_settings")
        return typing.cast(typing.Optional["ComputeBackendServiceSecuritySettings"], result)

    @builtins.property
    def service_lb_policy(self) -> typing.Optional[builtins.str]:
        '''URL to networkservices.ServiceLbPolicy resource. Can only be set if load balancing scheme is EXTERNAL, EXTERNAL_MANAGED, INTERNAL_MANAGED or INTERNAL_SELF_MANAGED and the scope is global.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#service_lb_policy ComputeBackendService#service_lb_policy}
        '''
        result = self._values.get("service_lb_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_affinity(self) -> typing.Optional[builtins.str]:
        '''Type of session affinity to use.

        The default is NONE. Session affinity is
        not applicable if the protocol is UDP. Possible values: ["NONE", "CLIENT_IP", "CLIENT_IP_PORT_PROTO", "CLIENT_IP_PROTO", "GENERATED_COOKIE", "HEADER_FIELD", "HTTP_COOKIE", "STRONG_COOKIE_AFFINITY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#session_affinity ComputeBackendService#session_affinity}
        '''
        result = self._values.get("session_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strong_session_affinity_cookie(
        self,
    ) -> typing.Optional["ComputeBackendServiceStrongSessionAffinityCookie"]:
        '''strong_session_affinity_cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#strong_session_affinity_cookie ComputeBackendService#strong_session_affinity_cookie}
        '''
        result = self._values.get("strong_session_affinity_cookie")
        return typing.cast(typing.Optional["ComputeBackendServiceStrongSessionAffinityCookie"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeBackendServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#timeouts ComputeBackendService#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeBackendServiceTimeouts"], result)

    @builtins.property
    def timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''The backend service timeout has a different meaning depending on the type of load balancer.

        For more information see, `Backend service settings <https://cloud.google.com/compute/docs/reference/rest/v1/backendServices>`_.
        The default is 30 seconds.
        The full range of timeout values allowed goes from 1 through 2,147,483,647 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#timeout_sec ComputeBackendService#timeout_sec}
        '''
        result = self._values.get("timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tls_settings(self) -> typing.Optional["ComputeBackendServiceTlsSettings"]:
        '''tls_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#tls_settings ComputeBackendService#tls_settings}
        '''
        result = self._values.get("tls_settings")
        return typing.cast(typing.Optional["ComputeBackendServiceTlsSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceConsistentHash",
    jsii_struct_bases=[],
    name_mapping={
        "http_cookie": "httpCookie",
        "http_header_name": "httpHeaderName",
        "minimum_ring_size": "minimumRingSize",
    },
)
class ComputeBackendServiceConsistentHash:
    def __init__(
        self,
        *,
        http_cookie: typing.Optional[typing.Union["ComputeBackendServiceConsistentHashHttpCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        http_header_name: typing.Optional[builtins.str] = None,
        minimum_ring_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_cookie: http_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#http_cookie ComputeBackendService#http_cookie}
        :param http_header_name: The hash based on the value of the specified header field. This field is applicable if the sessionAffinity is set to HEADER_FIELD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#http_header_name ComputeBackendService#http_header_name}
        :param minimum_ring_size: The minimum number of virtual nodes to use for the hash ring. Larger ring sizes result in more granular load distributions. If the number of hosts in the load balancing pool is larger than the ring size, each host will be assigned a single virtual node. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#minimum_ring_size ComputeBackendService#minimum_ring_size}
        '''
        if isinstance(http_cookie, dict):
            http_cookie = ComputeBackendServiceConsistentHashHttpCookie(**http_cookie)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24249d474b94c3417b540849d329bc41c585129641ce6113b30c323aa69413d3)
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
    ) -> typing.Optional["ComputeBackendServiceConsistentHashHttpCookie"]:
        '''http_cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#http_cookie ComputeBackendService#http_cookie}
        '''
        result = self._values.get("http_cookie")
        return typing.cast(typing.Optional["ComputeBackendServiceConsistentHashHttpCookie"], result)

    @builtins.property
    def http_header_name(self) -> typing.Optional[builtins.str]:
        '''The hash based on the value of the specified header field.

        This field is applicable if the sessionAffinity is set to HEADER_FIELD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#http_header_name ComputeBackendService#http_header_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#minimum_ring_size ComputeBackendService#minimum_ring_size}
        '''
        result = self._values.get("minimum_ring_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceConsistentHash(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceConsistentHashHttpCookie",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "ttl": "ttl"},
)
class ComputeBackendServiceConsistentHashHttpCookie:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[typing.Union["ComputeBackendServiceConsistentHashHttpCookieTtl", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#path ComputeBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#ttl ComputeBackendService#ttl}
        '''
        if isinstance(ttl, dict):
            ttl = ComputeBackendServiceConsistentHashHttpCookieTtl(**ttl)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5768d1136f62b838c574b16145c7188201288dafb98c03e5578ceb10e2337561)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to set for the cookie.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#path ComputeBackendService#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(
        self,
    ) -> typing.Optional["ComputeBackendServiceConsistentHashHttpCookieTtl"]:
        '''ttl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#ttl ComputeBackendService#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional["ComputeBackendServiceConsistentHashHttpCookieTtl"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceConsistentHashHttpCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceConsistentHashHttpCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceConsistentHashHttpCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dc9a69f0721dcf414346aa584cf38f51237774dee2cc229063c568e860b6047)
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#seconds ComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#nanos ComputeBackendService#nanos}
        '''
        value = ComputeBackendServiceConsistentHashHttpCookieTtl(
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
    def ttl(self) -> "ComputeBackendServiceConsistentHashHttpCookieTtlOutputReference":
        return typing.cast("ComputeBackendServiceConsistentHashHttpCookieTtlOutputReference", jsii.get(self, "ttl"))

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
    ) -> typing.Optional["ComputeBackendServiceConsistentHashHttpCookieTtl"]:
        return typing.cast(typing.Optional["ComputeBackendServiceConsistentHashHttpCookieTtl"], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b6129fd0530717d7336d4da91f11dfe51cd66bc046d526a65e35e475e185e05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7152ac7f26e0caadc237699d96122fd12f8a17f89460ad3fd259d58ccf21f607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeBackendServiceConsistentHashHttpCookie]:
        return typing.cast(typing.Optional[ComputeBackendServiceConsistentHashHttpCookie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceConsistentHashHttpCookie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1afc370d2255683a0cec6e2b9515ad8d3240fbb49f0d5cf2fdc4de57f7fe3404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceConsistentHashHttpCookieTtl",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeBackendServiceConsistentHashHttpCookieTtl:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#seconds ComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#nanos ComputeBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cfcf0c79c0d13aa2f67b889ee04395156d17df1d9e0babfc3e4deef93b23770)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#seconds ComputeBackendService#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#nanos ComputeBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceConsistentHashHttpCookieTtl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceConsistentHashHttpCookieTtlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceConsistentHashHttpCookieTtlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35c8b8be840be8b0f5a21e055c712ab5850d9b290075406082badd5c426689a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36e932d49ab438f3da6fcece89f6db9fcd10bf8df83f528fd6c95ab38cc5099c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f7a1e22dc98a1d55244cb1347812bfd6f6c58a1316594f41888c9d93231331f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeBackendServiceConsistentHashHttpCookieTtl]:
        return typing.cast(typing.Optional[ComputeBackendServiceConsistentHashHttpCookieTtl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceConsistentHashHttpCookieTtl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7773f8dd09c4d1b66a0fb03e8536572a02ed9ebaf6a1791616bf75f737ae0f26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendServiceConsistentHashOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceConsistentHashOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56fb90af6a3f12a1a032cd8344bc6ac7ad2437cfe63ff782cf6ad42bc96f0f73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpCookie")
    def put_http_cookie(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[typing.Union[ComputeBackendServiceConsistentHashHttpCookieTtl, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#path ComputeBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#ttl ComputeBackendService#ttl}
        '''
        value = ComputeBackendServiceConsistentHashHttpCookie(
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
    ) -> ComputeBackendServiceConsistentHashHttpCookieOutputReference:
        return typing.cast(ComputeBackendServiceConsistentHashHttpCookieOutputReference, jsii.get(self, "httpCookie"))

    @builtins.property
    @jsii.member(jsii_name="httpCookieInput")
    def http_cookie_input(
        self,
    ) -> typing.Optional[ComputeBackendServiceConsistentHashHttpCookie]:
        return typing.cast(typing.Optional[ComputeBackendServiceConsistentHashHttpCookie], jsii.get(self, "httpCookieInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5dc7608d0727dcf8af90febc6a547d6630dadfdcb3e67429be98139cb06067ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumRingSize")
    def minimum_ring_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumRingSize"))

    @minimum_ring_size.setter
    def minimum_ring_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b99cb7a514f000754cc3b912d8a88fe4ea59aa8fef20de3cec7826ee1140a8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumRingSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeBackendServiceConsistentHash]:
        return typing.cast(typing.Optional[ComputeBackendServiceConsistentHash], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceConsistentHash],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f50b2e209cf84d1bcb9963bbaea103840c94627ccd23e75cd11cea81fc0a9cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceCustomMetrics",
    jsii_struct_bases=[],
    name_mapping={"dry_run": "dryRun", "name": "name"},
)
class ComputeBackendServiceCustomMetrics:
    def __init__(
        self,
        *,
        dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
    ) -> None:
        '''
        :param dry_run: If true, the metric data is not used for load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#dry_run ComputeBackendService#dry_run}
        :param name: Name of a custom utilization signal. The name must be 1-64 characters long and match the regular expression `a-z <%5B-_.a-z0-9%5D*%5Ba-z0-9%5D>`_? which means the first character must be a lowercase letter, and all following characters must be a dash, period, underscore, lowercase letter, or digit, except the last character, which cannot be a dash, period, or underscore. For usage guidelines, see Custom Metrics balancing mode. This field can only be used for a global or regional backend service with the loadBalancingScheme set to EXTERNAL_MANAGED, INTERNAL_MANAGED INTERNAL_SELF_MANAGED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f72eae0a6616c2645a2bf67b5e7ad93c83ea1dc172e67318108bd88c5768b90)
            check_type(argname="argument dry_run", value=dry_run, expected_type=type_hints["dry_run"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dry_run": dry_run,
            "name": name,
        }

    @builtins.property
    def dry_run(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, the metric data is not used for load balancing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#dry_run ComputeBackendService#dry_run}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceCustomMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceCustomMetricsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceCustomMetricsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfd241ee729fe74f60c9b8d9b40375fbb7cdb3fed5dc50e8cdbdb472a371dd6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeBackendServiceCustomMetricsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f7d5529c8ab1992e0c9aa4c00affa1ae844ec57c31e8e1b3ca2878329e74543)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeBackendServiceCustomMetricsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ed245cdf2cb4f2e9ec9b786694bd97a26722b0bf9671f8da3dbb33365c2c43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9104840a743b8ff0172d046d1da375c9e6c2ee8ffcb0ef2f5c2b754768ac17e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__470202cdc8867572b7f9e9af73d0578fcb8ea91e5bc0c2919ee849913a078d92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCustomMetrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCustomMetrics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCustomMetrics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7622d1db5f82075877a1e4649c2f6bf9d1ddca4670bbe1135b4d3522893dbec8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendServiceCustomMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceCustomMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__160f8b263ab2dbea0b4178319f661b6a6e3afaff421517a3d9a58d48e929b6be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b464bedf82720fd7fbf9318e8d0b55b3f466960519c1518eb79da6eabe420cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dryRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a3dd17be65a5e6ccc995acaf7d41728a2694839023df512011deefecf4765b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceCustomMetrics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceCustomMetrics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceCustomMetrics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7e19c08710afac8058116876f0b96bae4d5bb80e8761132ade854808c445845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceIap",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "oauth2_client_id": "oauth2ClientId",
        "oauth2_client_secret": "oauth2ClientSecret",
    },
)
class ComputeBackendServiceIap:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        oauth2_client_id: typing.Optional[builtins.str] = None,
        oauth2_client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Whether the serving infrastructure will authenticate and authorize all incoming requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enabled ComputeBackendService#enabled}
        :param oauth2_client_id: OAuth2 Client ID for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#oauth2_client_id ComputeBackendService#oauth2_client_id}
        :param oauth2_client_secret: OAuth2 Client Secret for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#oauth2_client_secret ComputeBackendService#oauth2_client_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db6a067a9c2bb1e490175d2888e307496906618b95fd5aaf9f8986908ed6a63)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enabled ComputeBackendService#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def oauth2_client_id(self) -> typing.Optional[builtins.str]:
        '''OAuth2 Client ID for IAP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#oauth2_client_id ComputeBackendService#oauth2_client_id}
        '''
        result = self._values.get("oauth2_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth2_client_secret(self) -> typing.Optional[builtins.str]:
        '''OAuth2 Client Secret for IAP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#oauth2_client_secret ComputeBackendService#oauth2_client_secret}
        '''
        result = self._values.get("oauth2_client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceIap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceIapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceIapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abded96dff214f1d51b58ff01b54751f2bba1ef36785b96d14140d4cc2b4af3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82ea67c9f0e091e51c97a0921de7eb5c7ce85853d368855bec0ec7f2fedaa8ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientId")
    def oauth2_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2ClientId"))

    @oauth2_client_id.setter
    def oauth2_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2daa88fdf2922ef32100c14a14547f8b2df605964a354cc274130f590ae2d2a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauth2ClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientSecret")
    def oauth2_client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2ClientSecret"))

    @oauth2_client_secret.setter
    def oauth2_client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b53be0989d8177aff045165d8112e47fb1bc0d95d1062e33a998fb756632f85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauth2ClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeBackendServiceIap]:
        return typing.cast(typing.Optional[ComputeBackendServiceIap], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeBackendServiceIap]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c22502ece2e3bec3c41b02c6a50f4f861fd6c92bb78f6806986a79b5ed180bf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceLocalityLbPolicies",
    jsii_struct_bases=[],
    name_mapping={"custom_policy": "customPolicy", "policy": "policy"},
)
class ComputeBackendServiceLocalityLbPolicies:
    def __init__(
        self,
        *,
        custom_policy: typing.Optional[typing.Union["ComputeBackendServiceLocalityLbPoliciesCustomPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        policy: typing.Optional[typing.Union["ComputeBackendServiceLocalityLbPoliciesPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_policy: custom_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#custom_policy ComputeBackendService#custom_policy}
        :param policy: policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#policy ComputeBackendService#policy}
        '''
        if isinstance(custom_policy, dict):
            custom_policy = ComputeBackendServiceLocalityLbPoliciesCustomPolicy(**custom_policy)
        if isinstance(policy, dict):
            policy = ComputeBackendServiceLocalityLbPoliciesPolicy(**policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__133b9c63a29d398d55f5e8aa6d1e3436d6cde27a2e9e345f7cf0094105fdf2e7)
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
    ) -> typing.Optional["ComputeBackendServiceLocalityLbPoliciesCustomPolicy"]:
        '''custom_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#custom_policy ComputeBackendService#custom_policy}
        '''
        result = self._values.get("custom_policy")
        return typing.cast(typing.Optional["ComputeBackendServiceLocalityLbPoliciesCustomPolicy"], result)

    @builtins.property
    def policy(
        self,
    ) -> typing.Optional["ComputeBackendServiceLocalityLbPoliciesPolicy"]:
        '''policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#policy ComputeBackendService#policy}
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional["ComputeBackendServiceLocalityLbPoliciesPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceLocalityLbPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceLocalityLbPoliciesCustomPolicy",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "data": "data"},
)
class ComputeBackendServiceLocalityLbPoliciesCustomPolicy:
    def __init__(
        self,
        *,
        name: builtins.str,
        data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Identifies the custom policy. The value should match the type the custom implementation is registered with on the gRPC clients. It should follow protocol buffer message naming conventions and include the full path (e.g. myorg.CustomLbPolicy). The maximum length is 256 characters. Note that specifying the same custom policy more than once for a backend is not a valid configuration and will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        :param data: An optional, arbitrary JSON object with configuration data, understood by a locally installed custom policy implementation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#data ComputeBackendService#data}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78a181450b18a2ff77a72f97f47cba6f914360aeaa61388eb73dd3670239fad8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''An optional, arbitrary JSON object with configuration data, understood by a locally installed custom policy implementation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#data ComputeBackendService#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceLocalityLbPoliciesCustomPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceLocalityLbPoliciesCustomPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceLocalityLbPoliciesCustomPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__153b2c3cd822a8ba70a6135036a50c4bc23bd0e55b4b4a0110cc0568f5c7b380)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d38e3b6c8a27e09b83f8a509690ea0460cfeb35369f51eaa5934d6a9842f8bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b537cb6cf6fa652c76c374b0c9fca7a4e8eb3d1c4fafd294b8cc12dd001d196d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeBackendServiceLocalityLbPoliciesCustomPolicy]:
        return typing.cast(typing.Optional[ComputeBackendServiceLocalityLbPoliciesCustomPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceLocalityLbPoliciesCustomPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f16611013386bb50dc0f5ad76f228b3aa080a48261f12673179be1b649d6767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendServiceLocalityLbPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceLocalityLbPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f4f5dcb2702ce35c18a835f83a1ba36275af06539f75cf783f2130d1e11cd28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeBackendServiceLocalityLbPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4ff33eb1c2c47ef399616f912d2b56a382bea2a265a0f380d1d8856ebe1fa44)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeBackendServiceLocalityLbPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df52b34431c2035337c295e686bf27801fc9d3a87e9b0f5710bbf1bce6d0ac94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2913986f2e4889fb96ef60840c6db5eec594b07c093f6edc1838fca6a00303d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2887e2527250450f62fbe796870e84cf7cebec946473baa844b9971c7f1237d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceLocalityLbPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceLocalityLbPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceLocalityLbPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ba32ebb1c0dedd3033d22e1fc94c33164e322c3d7a15f50369826eea8092e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendServiceLocalityLbPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceLocalityLbPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__349563c70352b761154e31a1fa0a9745846386dbfec2b51edc5b083e6f5fe641)
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
        :param name: Identifies the custom policy. The value should match the type the custom implementation is registered with on the gRPC clients. It should follow protocol buffer message naming conventions and include the full path (e.g. myorg.CustomLbPolicy). The maximum length is 256 characters. Note that specifying the same custom policy more than once for a backend is not a valid configuration and will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        :param data: An optional, arbitrary JSON object with configuration data, understood by a locally installed custom policy implementation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#data ComputeBackendService#data}
        '''
        value = ComputeBackendServiceLocalityLbPoliciesCustomPolicy(
            name=name, data=data
        )

        return typing.cast(None, jsii.invoke(self, "putCustomPolicy", [value]))

    @jsii.member(jsii_name="putPolicy")
    def put_policy(self, *, name: builtins.str) -> None:
        '''
        :param name: The name of a locality load balancer policy to be used. The value should be one of the predefined ones as supported by localityLbPolicy, although at the moment only ROUND_ROBIN is supported. This field should only be populated when the customPolicy field is not used. Note that specifying the same policy more than once for a backend is not a valid configuration and will be rejected. The possible values are: - 'ROUND_ROBIN': This is a simple policy in which each healthy backend is selected in round robin order. - 'LEAST_REQUEST': An O(1) algorithm which selects two random healthy hosts and picks the host which has fewer active requests. - 'RING_HASH': The ring/modulo hash load balancer implements consistent hashing to backends. The algorithm has the property that the addition/removal of a host from a set of N hosts only affects 1/N of the requests. - 'RANDOM': The load balancer selects a random healthy host. - 'ORIGINAL_DESTINATION': Backend host is selected based on the client connection metadata, i.e., connections are opened to the same address as the destination address of the incoming connection before the connection was redirected to the load balancer. - 'MAGLEV': used as a drop in replacement for the ring hash load balancer. Maglev is not as stable as ring hash but has faster table lookup build times and host selection times. For more information about Maglev, refer to https://ai.google/research/pubs/pub44824 Possible values: ["ROUND_ROBIN", "LEAST_REQUEST", "RING_HASH", "RANDOM", "ORIGINAL_DESTINATION", "MAGLEV"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        '''
        value = ComputeBackendServiceLocalityLbPoliciesPolicy(name=name)

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
    ) -> ComputeBackendServiceLocalityLbPoliciesCustomPolicyOutputReference:
        return typing.cast(ComputeBackendServiceLocalityLbPoliciesCustomPolicyOutputReference, jsii.get(self, "customPolicy"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> "ComputeBackendServiceLocalityLbPoliciesPolicyOutputReference":
        return typing.cast("ComputeBackendServiceLocalityLbPoliciesPolicyOutputReference", jsii.get(self, "policy"))

    @builtins.property
    @jsii.member(jsii_name="customPolicyInput")
    def custom_policy_input(
        self,
    ) -> typing.Optional[ComputeBackendServiceLocalityLbPoliciesCustomPolicy]:
        return typing.cast(typing.Optional[ComputeBackendServiceLocalityLbPoliciesCustomPolicy], jsii.get(self, "customPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(
        self,
    ) -> typing.Optional["ComputeBackendServiceLocalityLbPoliciesPolicy"]:
        return typing.cast(typing.Optional["ComputeBackendServiceLocalityLbPoliciesPolicy"], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceLocalityLbPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceLocalityLbPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceLocalityLbPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976e1bf01e8c4c7241575ae7e460d2671175995d73a83293c4d56024abb7ad11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceLocalityLbPoliciesPolicy",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ComputeBackendServiceLocalityLbPoliciesPolicy:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: The name of a locality load balancer policy to be used. The value should be one of the predefined ones as supported by localityLbPolicy, although at the moment only ROUND_ROBIN is supported. This field should only be populated when the customPolicy field is not used. Note that specifying the same policy more than once for a backend is not a valid configuration and will be rejected. The possible values are: - 'ROUND_ROBIN': This is a simple policy in which each healthy backend is selected in round robin order. - 'LEAST_REQUEST': An O(1) algorithm which selects two random healthy hosts and picks the host which has fewer active requests. - 'RING_HASH': The ring/modulo hash load balancer implements consistent hashing to backends. The algorithm has the property that the addition/removal of a host from a set of N hosts only affects 1/N of the requests. - 'RANDOM': The load balancer selects a random healthy host. - 'ORIGINAL_DESTINATION': Backend host is selected based on the client connection metadata, i.e., connections are opened to the same address as the destination address of the incoming connection before the connection was redirected to the load balancer. - 'MAGLEV': used as a drop in replacement for the ring hash load balancer. Maglev is not as stable as ring hash but has faster table lookup build times and host selection times. For more information about Maglev, refer to https://ai.google/research/pubs/pub44824 Possible values: ["ROUND_ROBIN", "LEAST_REQUEST", "RING_HASH", "RANDOM", "ORIGINAL_DESTINATION", "MAGLEV"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2a96fb847d7ef407f55e7fd8c058cfa85c50497de5475c94ee8c1df0592ea1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceLocalityLbPoliciesPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceLocalityLbPoliciesPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceLocalityLbPoliciesPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a5f1182a2241adb700a51d3217e3a5d00c80eaaa0b7f63c02c858a2d383190a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56a30b0b63005c8f1d6582949fc38e5ece28c9349400f012d4d9222c39eb6e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeBackendServiceLocalityLbPoliciesPolicy]:
        return typing.cast(typing.Optional[ComputeBackendServiceLocalityLbPoliciesPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceLocalityLbPoliciesPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45e3f918bea2e83a5679077d4c61d9116818042031f9d3f34042d893c2a63a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceLogConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable": "enable",
        "optional_fields": "optionalFields",
        "optional_mode": "optionalMode",
        "sample_rate": "sampleRate",
    },
)
class ComputeBackendServiceLogConfig:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        optional_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        optional_mode: typing.Optional[builtins.str] = None,
        sample_rate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enable: Whether to enable logging for the load balancer traffic served by this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enable ComputeBackendService#enable}
        :param optional_fields: This field can only be specified if logging is enabled for this backend service and "logConfig.optionalMode" was set to CUSTOM. Contains a list of optional fields you want to include in the logs. For example: serverInstance, serverGkeDetails.cluster, serverGkeDetails.pod.podNamespace For example: orca_load_report, tls.protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#optional_fields ComputeBackendService#optional_fields}
        :param optional_mode: Specifies the optional logging mode for the load balancer traffic. Supported values: INCLUDE_ALL_OPTIONAL, EXCLUDE_ALL_OPTIONAL, CUSTOM. Possible values: ["INCLUDE_ALL_OPTIONAL", "EXCLUDE_ALL_OPTIONAL", "CUSTOM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#optional_mode ComputeBackendService#optional_mode}
        :param sample_rate: This field can only be specified if logging is enabled for this backend service. The value of the field must be in [0, 1]. This configures the sampling rate of requests to the load balancer where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported. The default value is 1.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#sample_rate ComputeBackendService#sample_rate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99b387fa30cf77c6d12fba5a600b2b14d0e573d800567f0c9fec0fe7280d0ab8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enable ComputeBackendService#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def optional_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''This field can only be specified if logging is enabled for this backend service and "logConfig.optionalMode" was set to CUSTOM. Contains a list of optional fields you want to include in the logs. For example: serverInstance, serverGkeDetails.cluster, serverGkeDetails.pod.podNamespace For example: orca_load_report, tls.protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#optional_fields ComputeBackendService#optional_fields}
        '''
        result = self._values.get("optional_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def optional_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the optional logging mode for the load balancer traffic. Supported values: INCLUDE_ALL_OPTIONAL, EXCLUDE_ALL_OPTIONAL, CUSTOM. Possible values: ["INCLUDE_ALL_OPTIONAL", "EXCLUDE_ALL_OPTIONAL", "CUSTOM"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#optional_mode ComputeBackendService#optional_mode}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#sample_rate ComputeBackendService#sample_rate}
        '''
        result = self._values.get("sample_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__519f8a5f09ccbf1f31b71ec1052c98a84a673f49d9dd31c17c8c157cbcda76cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc3ac8736b55b88237f7a5d9f52ec5dc98c3dbf3d26c51dacc9c6a0bce82f577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optionalFields")
    def optional_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "optionalFields"))

    @optional_fields.setter
    def optional_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8428bfb9a93c42eae890039a7452f56da7c195d1e7b2af8c1f420d119954dfd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionalFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optionalMode")
    def optional_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "optionalMode"))

    @optional_mode.setter
    def optional_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e9a371cc45970994928b6baadb48324cb38061405666c3c1adef76f1d6ec39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionalMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleRate")
    def sample_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleRate"))

    @sample_rate.setter
    def sample_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a0a0b451fa7e0a5df9ea96341586659540e7512c4adf7685a2af38755bbb50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeBackendServiceLogConfig]:
        return typing.cast(typing.Optional[ComputeBackendServiceLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2bd8556fed1a7aacebe1feb97fcefe1e6f62e5af4be5d1a36aa3bac171187c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceMaxStreamDuration",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeBackendServiceMaxStreamDuration:
    def __init__(
        self,
        *,
        seconds: builtins.str,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. (int64 format). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#seconds ComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#nanos ComputeBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6210bab88f06770c9a44434e10ca3c48da4072e02de6effe4d309353f56ce161)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#seconds ComputeBackendService#seconds}
        '''
        result = self._values.get("seconds")
        assert result is not None, "Required property 'seconds' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Span of time that's a fraction of a second at nanosecond resolution.

        Durations less than one second are represented with a 0 seconds field and a positive nanos field.
        Must be from 0 to 999,999,999 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#nanos ComputeBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceMaxStreamDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceMaxStreamDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceMaxStreamDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85cb9cb82159a00e840111ffa210a705deebe1bee6a403d6fc65203bfe1836bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39d3f5de690679adee476e35ff0f759efa983b4355c8edea0996f3880a0514ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8fe3b7074dc52c4068aa2399407fe8a71d0e9f9babd577988eed62da323602b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeBackendServiceMaxStreamDuration]:
        return typing.cast(typing.Optional[ComputeBackendServiceMaxStreamDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceMaxStreamDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353f8f4466a866472d52c6733c4ba623730f62cabfe389007797e204c9d35c10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceOutlierDetection",
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
class ComputeBackendServiceOutlierDetection:
    def __init__(
        self,
        *,
        base_ejection_time: typing.Optional[typing.Union["ComputeBackendServiceOutlierDetectionBaseEjectionTime", typing.Dict[builtins.str, typing.Any]]] = None,
        consecutive_errors: typing.Optional[jsii.Number] = None,
        consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_errors: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_success_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[typing.Union["ComputeBackendServiceOutlierDetectionInterval", typing.Dict[builtins.str, typing.Any]]] = None,
        max_ejection_percent: typing.Optional[jsii.Number] = None,
        success_rate_minimum_hosts: typing.Optional[jsii.Number] = None,
        success_rate_request_volume: typing.Optional[jsii.Number] = None,
        success_rate_stdev_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param base_ejection_time: base_ejection_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#base_ejection_time ComputeBackendService#base_ejection_time}
        :param consecutive_errors: Number of errors before a host is ejected from the connection pool. When the backend host is accessed over HTTP, a 5xx return code qualifies as an error. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#consecutive_errors ComputeBackendService#consecutive_errors}
        :param consecutive_gateway_failure: The number of consecutive gateway failures (502, 503, 504 status or connection errors that are mapped to one of those status codes) before a consecutive gateway failure ejection occurs. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#consecutive_gateway_failure ComputeBackendService#consecutive_gateway_failure}
        :param enforcing_consecutive_errors: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive 5xx. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enforcing_consecutive_errors ComputeBackendService#enforcing_consecutive_errors}
        :param enforcing_consecutive_gateway_failure: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive gateway failures. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enforcing_consecutive_gateway_failure ComputeBackendService#enforcing_consecutive_gateway_failure}
        :param enforcing_success_rate: The percentage chance that a host will be actually ejected when an outlier status is detected through success rate statistics. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enforcing_success_rate ComputeBackendService#enforcing_success_rate}
        :param interval: interval block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#interval ComputeBackendService#interval}
        :param max_ejection_percent: Maximum percentage of hosts in the load balancing pool for the backend service that can be ejected. Defaults to 10%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_ejection_percent ComputeBackendService#max_ejection_percent}
        :param success_rate_minimum_hosts: The number of hosts in a cluster that must have enough request volume to detect success rate outliers. If the number of hosts is less than this setting, outlier detection via success rate statistics is not performed for any host in the cluster. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#success_rate_minimum_hosts ComputeBackendService#success_rate_minimum_hosts}
        :param success_rate_request_volume: The minimum number of total requests that must be collected in one interval (as defined by the interval duration above) to include this host in success rate based outlier detection. If the volume is lower than this setting, outlier detection via success rate statistics is not performed for that host. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#success_rate_request_volume ComputeBackendService#success_rate_request_volume}
        :param success_rate_stdev_factor: This factor is used to determine the ejection threshold for success rate outlier ejection. The ejection threshold is the difference between the mean success rate, and the product of this factor and the standard deviation of the mean success rate: mean - (stdev * success_rate_stdev_factor). This factor is divided by a thousand to get a double. That is, if the desired factor is 1.9, the runtime value should be 1900. Defaults to 1900. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#success_rate_stdev_factor ComputeBackendService#success_rate_stdev_factor}
        '''
        if isinstance(base_ejection_time, dict):
            base_ejection_time = ComputeBackendServiceOutlierDetectionBaseEjectionTime(**base_ejection_time)
        if isinstance(interval, dict):
            interval = ComputeBackendServiceOutlierDetectionInterval(**interval)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4c3d24e022e54b5a59882f6b33ab107c28418b401ee4a0357f8fc66c41b2cb3)
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
    ) -> typing.Optional["ComputeBackendServiceOutlierDetectionBaseEjectionTime"]:
        '''base_ejection_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#base_ejection_time ComputeBackendService#base_ejection_time}
        '''
        result = self._values.get("base_ejection_time")
        return typing.cast(typing.Optional["ComputeBackendServiceOutlierDetectionBaseEjectionTime"], result)

    @builtins.property
    def consecutive_errors(self) -> typing.Optional[jsii.Number]:
        '''Number of errors before a host is ejected from the connection pool.

        When the
        backend host is accessed over HTTP, a 5xx return code qualifies as an error.
        Defaults to 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#consecutive_errors ComputeBackendService#consecutive_errors}
        '''
        result = self._values.get("consecutive_errors")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def consecutive_gateway_failure(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive gateway failures (502, 503, 504 status or connection errors that are mapped to one of those status codes) before a consecutive gateway failure ejection occurs.

        Defaults to 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#consecutive_gateway_failure ComputeBackendService#consecutive_gateway_failure}
        '''
        result = self._values.get("consecutive_gateway_failure")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enforcing_consecutive_errors(self) -> typing.Optional[jsii.Number]:
        '''The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive 5xx.

        This setting can be used to disable
        ejection or to ramp it up slowly. Defaults to 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enforcing_consecutive_errors ComputeBackendService#enforcing_consecutive_errors}
        '''
        result = self._values.get("enforcing_consecutive_errors")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enforcing_consecutive_gateway_failure(self) -> typing.Optional[jsii.Number]:
        '''The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive gateway failures.

        This setting can be
        used to disable ejection or to ramp it up slowly. Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enforcing_consecutive_gateway_failure ComputeBackendService#enforcing_consecutive_gateway_failure}
        '''
        result = self._values.get("enforcing_consecutive_gateway_failure")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enforcing_success_rate(self) -> typing.Optional[jsii.Number]:
        '''The percentage chance that a host will be actually ejected when an outlier status is detected through success rate statistics.

        This setting can be used to
        disable ejection or to ramp it up slowly. Defaults to 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#enforcing_success_rate ComputeBackendService#enforcing_success_rate}
        '''
        result = self._values.get("enforcing_success_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(
        self,
    ) -> typing.Optional["ComputeBackendServiceOutlierDetectionInterval"]:
        '''interval block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#interval ComputeBackendService#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional["ComputeBackendServiceOutlierDetectionInterval"], result)

    @builtins.property
    def max_ejection_percent(self) -> typing.Optional[jsii.Number]:
        '''Maximum percentage of hosts in the load balancing pool for the backend service that can be ejected. Defaults to 10%.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#max_ejection_percent ComputeBackendService#max_ejection_percent}
        '''
        result = self._values.get("max_ejection_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_rate_minimum_hosts(self) -> typing.Optional[jsii.Number]:
        '''The number of hosts in a cluster that must have enough request volume to detect success rate outliers.

        If the number of hosts is less than this setting, outlier
        detection via success rate statistics is not performed for any host in the
        cluster. Defaults to 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#success_rate_minimum_hosts ComputeBackendService#success_rate_minimum_hosts}
        '''
        result = self._values.get("success_rate_minimum_hosts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_rate_request_volume(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of total requests that must be collected in one interval (as defined by the interval duration above) to include this host in success rate based outlier detection.

        If the volume is lower than this setting, outlier
        detection via success rate statistics is not performed for that host. Defaults
        to 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#success_rate_request_volume ComputeBackendService#success_rate_request_volume}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#success_rate_stdev_factor ComputeBackendService#success_rate_stdev_factor}
        '''
        result = self._values.get("success_rate_stdev_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceOutlierDetection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceOutlierDetectionBaseEjectionTime",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeBackendServiceOutlierDetectionBaseEjectionTime:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#seconds ComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#nanos ComputeBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3662efd40c09f95427a97d2217dcc0b97b81d63422d2b868ebb9075becba9260)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#seconds ComputeBackendService#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#nanos ComputeBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceOutlierDetectionBaseEjectionTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceOutlierDetectionBaseEjectionTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceOutlierDetectionBaseEjectionTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21b177162f774fd4730a19210b219bad426dcff46192144fefd0c786f1ab8268)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39ecef76a7fae9622c29aa19a03ec1b816a05306ed1e7f29b69de3da62924f35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ccce62b190a3b654b4765c9dbc5a232713c2d31be90cc91908cb2ac32c4d86e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeBackendServiceOutlierDetectionBaseEjectionTime]:
        return typing.cast(typing.Optional[ComputeBackendServiceOutlierDetectionBaseEjectionTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceOutlierDetectionBaseEjectionTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b56ab9820d66f5e91a2aecf74b94d38038eab423878bc48cf5d3c0607c154960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceOutlierDetectionInterval",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeBackendServiceOutlierDetectionInterval:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#seconds ComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#nanos ComputeBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd1d0c3b6bf832794859f2f7f9d7061de4d49f22cad232db8b386a825c7347b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#seconds ComputeBackendService#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#nanos ComputeBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceOutlierDetectionInterval(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceOutlierDetectionIntervalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceOutlierDetectionIntervalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91f4c5f0af97292ee12a9e45b60b6de1de7660defea3d9a37829d07b0c2efb15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81230bfc5b088b7c9795bf85651cef7f0b69a45592828219d328556c13b18e6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee116e28f96f3106bf14cf5bbbfc23d1a423b98cebe86646a7e4485cdfc46eac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeBackendServiceOutlierDetectionInterval]:
        return typing.cast(typing.Optional[ComputeBackendServiceOutlierDetectionInterval], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceOutlierDetectionInterval],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9460cbf2049c96fd7f500b8274ad2363d109c2aa4c984bbfd175bc82b997c184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendServiceOutlierDetectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceOutlierDetectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e335509fc6272d824948829d1d640d984b69a2c28b9393e42b78f2ab2af0609)
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#seconds ComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#nanos ComputeBackendService#nanos}
        '''
        value = ComputeBackendServiceOutlierDetectionBaseEjectionTime(
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#seconds ComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#nanos ComputeBackendService#nanos}
        '''
        value = ComputeBackendServiceOutlierDetectionInterval(
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
    ) -> ComputeBackendServiceOutlierDetectionBaseEjectionTimeOutputReference:
        return typing.cast(ComputeBackendServiceOutlierDetectionBaseEjectionTimeOutputReference, jsii.get(self, "baseEjectionTime"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> ComputeBackendServiceOutlierDetectionIntervalOutputReference:
        return typing.cast(ComputeBackendServiceOutlierDetectionIntervalOutputReference, jsii.get(self, "interval"))

    @builtins.property
    @jsii.member(jsii_name="baseEjectionTimeInput")
    def base_ejection_time_input(
        self,
    ) -> typing.Optional[ComputeBackendServiceOutlierDetectionBaseEjectionTime]:
        return typing.cast(typing.Optional[ComputeBackendServiceOutlierDetectionBaseEjectionTime], jsii.get(self, "baseEjectionTimeInput"))

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
    ) -> typing.Optional[ComputeBackendServiceOutlierDetectionInterval]:
        return typing.cast(typing.Optional[ComputeBackendServiceOutlierDetectionInterval], jsii.get(self, "intervalInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0e8c05522ede1dd5530975f838dd85f01e8bbfc6a816e28b45802d14da5d6d0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consecutiveErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consecutiveGatewayFailure")
    def consecutive_gateway_failure(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "consecutiveGatewayFailure"))

    @consecutive_gateway_failure.setter
    def consecutive_gateway_failure(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a23aa1be1239d5feff22cf92795a1e0507c34fe46be7024273703ccea8f93c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consecutiveGatewayFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcingConsecutiveErrors")
    def enforcing_consecutive_errors(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "enforcingConsecutiveErrors"))

    @enforcing_consecutive_errors.setter
    def enforcing_consecutive_errors(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c86ab261cdc33bb4554de4c273bbb25e20ddc2fba7b45014c52de9fdf1f2c26a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcingConsecutiveErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcingConsecutiveGatewayFailure")
    def enforcing_consecutive_gateway_failure(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "enforcingConsecutiveGatewayFailure"))

    @enforcing_consecutive_gateway_failure.setter
    def enforcing_consecutive_gateway_failure(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18ed83fb6e7cc5f1f243d93a1f6426cf2e6e392f5ca81f59a8e125e92abda1b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcingConsecutiveGatewayFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcingSuccessRate")
    def enforcing_success_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "enforcingSuccessRate"))

    @enforcing_success_rate.setter
    def enforcing_success_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41dc4c1caefb84069ed0e71e47dea86aaa83ee22a67a709e2860c3eee7d2719b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcingSuccessRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxEjectionPercent")
    def max_ejection_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxEjectionPercent"))

    @max_ejection_percent.setter
    def max_ejection_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc717166afb5409882f4daf3e596592720c1aefafec6b1ae546acd8f29d8c3c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxEjectionPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successRateMinimumHosts")
    def success_rate_minimum_hosts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successRateMinimumHosts"))

    @success_rate_minimum_hosts.setter
    def success_rate_minimum_hosts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0aec2735d2942ceef833f71ef98561dd586063ce35ef677cdc36d47b27917b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successRateMinimumHosts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successRateRequestVolume")
    def success_rate_request_volume(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successRateRequestVolume"))

    @success_rate_request_volume.setter
    def success_rate_request_volume(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37fe617d93252699eddf26326c8d987a9494aac421c8fc82a680086b4ad9030e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successRateRequestVolume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successRateStdevFactor")
    def success_rate_stdev_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successRateStdevFactor"))

    @success_rate_stdev_factor.setter
    def success_rate_stdev_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7251c000500ede829be00f87ae8adac21d1c429dea6d97a395c46a8ba57361d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successRateStdevFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeBackendServiceOutlierDetection]:
        return typing.cast(typing.Optional[ComputeBackendServiceOutlierDetection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceOutlierDetection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__012559c26bbac5595967249d0084d85184c63347dde6fd8e9d5a5bcdcbb13e1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceSecuritySettings",
    jsii_struct_bases=[],
    name_mapping={
        "aws_v4_authentication": "awsV4Authentication",
        "client_tls_policy": "clientTlsPolicy",
        "subject_alt_names": "subjectAltNames",
    },
)
class ComputeBackendServiceSecuritySettings:
    def __init__(
        self,
        *,
        aws_v4_authentication: typing.Optional[typing.Union["ComputeBackendServiceSecuritySettingsAwsV4Authentication", typing.Dict[builtins.str, typing.Any]]] = None,
        client_tls_policy: typing.Optional[builtins.str] = None,
        subject_alt_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param aws_v4_authentication: aws_v4_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#aws_v4_authentication ComputeBackendService#aws_v4_authentication}
        :param client_tls_policy: ClientTlsPolicy is a resource that specifies how a client should authenticate connections to backends of a service. This resource itself does not affect configuration unless it is attached to a backend service resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#client_tls_policy ComputeBackendService#client_tls_policy}
        :param subject_alt_names: A list of alternate names to verify the subject identity in the certificate. If specified, the client will verify that the server certificate's subject alt name matches one of the specified values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#subject_alt_names ComputeBackendService#subject_alt_names}
        '''
        if isinstance(aws_v4_authentication, dict):
            aws_v4_authentication = ComputeBackendServiceSecuritySettingsAwsV4Authentication(**aws_v4_authentication)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cd617f036e6ba15b8492ca68c20a028b6c7af7395253176e59bc7f135ecb6b3)
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
    ) -> typing.Optional["ComputeBackendServiceSecuritySettingsAwsV4Authentication"]:
        '''aws_v4_authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#aws_v4_authentication ComputeBackendService#aws_v4_authentication}
        '''
        result = self._values.get("aws_v4_authentication")
        return typing.cast(typing.Optional["ComputeBackendServiceSecuritySettingsAwsV4Authentication"], result)

    @builtins.property
    def client_tls_policy(self) -> typing.Optional[builtins.str]:
        '''ClientTlsPolicy is a resource that specifies how a client should authenticate connections to backends of a service.

        This resource itself does not affect
        configuration unless it is attached to a backend service resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#client_tls_policy ComputeBackendService#client_tls_policy}
        '''
        result = self._values.get("client_tls_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_alt_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of alternate names to verify the subject identity in the certificate.

        If specified, the client will verify that the server certificate's subject
        alt name matches one of the specified values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#subject_alt_names ComputeBackendService#subject_alt_names}
        '''
        result = self._values.get("subject_alt_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceSecuritySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceSecuritySettingsAwsV4Authentication",
    jsii_struct_bases=[],
    name_mapping={
        "access_key": "accessKey",
        "access_key_id": "accessKeyId",
        "access_key_version": "accessKeyVersion",
        "origin_region": "originRegion",
    },
)
class ComputeBackendServiceSecuritySettingsAwsV4Authentication:
    def __init__(
        self,
        *,
        access_key: typing.Optional[builtins.str] = None,
        access_key_id: typing.Optional[builtins.str] = None,
        access_key_version: typing.Optional[builtins.str] = None,
        origin_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_key: The access key used for s3 bucket authentication. Required for updating or creating a backend that uses AWS v4 signature authentication, but will not be returned as part of the configuration when queried with a REST API GET request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#access_key ComputeBackendService#access_key}
        :param access_key_id: The identifier of an access key used for s3 bucket authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#access_key_id ComputeBackendService#access_key_id}
        :param access_key_version: The optional version identifier for the access key. You can use this to keep track of different iterations of your access key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#access_key_version ComputeBackendService#access_key_version}
        :param origin_region: The name of the cloud region of your origin. This is a free-form field with the name of the region your cloud uses to host your origin. For example, "us-east-1" for AWS or "us-ashburn-1" for OCI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#origin_region ComputeBackendService#origin_region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81791ca30ad8b119b0c9aa936cf81fbc3af5d157dd93b84c9d7bd38d7ad29cac)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#access_key ComputeBackendService#access_key}
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of an access key used for s3 bucket authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#access_key_id ComputeBackendService#access_key_id}
        '''
        result = self._values.get("access_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_key_version(self) -> typing.Optional[builtins.str]:
        '''The optional version identifier for the access key.

        You can use this to keep track of different iterations of your access key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#access_key_version ComputeBackendService#access_key_version}
        '''
        result = self._values.get("access_key_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_region(self) -> typing.Optional[builtins.str]:
        '''The name of the cloud region of your origin.

        This is a free-form field with the name of the region your cloud uses to host your origin.
        For example, "us-east-1" for AWS or "us-ashburn-1" for OCI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#origin_region ComputeBackendService#origin_region}
        '''
        result = self._values.get("origin_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceSecuritySettingsAwsV4Authentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceSecuritySettingsAwsV4AuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceSecuritySettingsAwsV4AuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56246216e26ae82b24579db5ad149d50faee9d434b6770bca15c610dc1cd5828)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4609b7312c0e5067c24b9be19ec7b28748aeb92d16ef85df5a5e32091c94706e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKeyId"))

    @access_key_id.setter
    def access_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395b36b6595f2680d5b9a9bd007ef63e876ef9862c65794a6b7386e710023be4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessKeyVersion")
    def access_key_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKeyVersion"))

    @access_key_version.setter
    def access_key_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975f888eb54839b2b82234e03dc73f267458965d186a50c5761c814b10529199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeyVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originRegion")
    def origin_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originRegion"))

    @origin_region.setter
    def origin_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56f3c5a1e550cddc802001ad627b99a7bdf7e875f2edee7b99cf17ef3a03f86f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeBackendServiceSecuritySettingsAwsV4Authentication]:
        return typing.cast(typing.Optional[ComputeBackendServiceSecuritySettingsAwsV4Authentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceSecuritySettingsAwsV4Authentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9caef7639dd8cb7bd6017cf5375450bc5ba1d00690627b4456b543efe17970d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendServiceSecuritySettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceSecuritySettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b91215240621f88f545852d5ce74e966883722e7653c3ce2a3c53d9d903f39ce)
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
        :param access_key: The access key used for s3 bucket authentication. Required for updating or creating a backend that uses AWS v4 signature authentication, but will not be returned as part of the configuration when queried with a REST API GET request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#access_key ComputeBackendService#access_key}
        :param access_key_id: The identifier of an access key used for s3 bucket authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#access_key_id ComputeBackendService#access_key_id}
        :param access_key_version: The optional version identifier for the access key. You can use this to keep track of different iterations of your access key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#access_key_version ComputeBackendService#access_key_version}
        :param origin_region: The name of the cloud region of your origin. This is a free-form field with the name of the region your cloud uses to host your origin. For example, "us-east-1" for AWS or "us-ashburn-1" for OCI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#origin_region ComputeBackendService#origin_region}
        '''
        value = ComputeBackendServiceSecuritySettingsAwsV4Authentication(
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
    ) -> ComputeBackendServiceSecuritySettingsAwsV4AuthenticationOutputReference:
        return typing.cast(ComputeBackendServiceSecuritySettingsAwsV4AuthenticationOutputReference, jsii.get(self, "awsV4Authentication"))

    @builtins.property
    @jsii.member(jsii_name="awsV4AuthenticationInput")
    def aws_v4_authentication_input(
        self,
    ) -> typing.Optional[ComputeBackendServiceSecuritySettingsAwsV4Authentication]:
        return typing.cast(typing.Optional[ComputeBackendServiceSecuritySettingsAwsV4Authentication], jsii.get(self, "awsV4AuthenticationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__56f3e1fa8dba24294768465ee0250a147c835080cd21deda3358bcecab7a0a9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTlsPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectAltNames")
    def subject_alt_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subjectAltNames"))

    @subject_alt_names.setter
    def subject_alt_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b046c1b0cae4789203d72db60d141646b4775ef6f24f0a947c4f57d7068bf78a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectAltNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeBackendServiceSecuritySettings]:
        return typing.cast(typing.Optional[ComputeBackendServiceSecuritySettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceSecuritySettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d84cb2cb1a53da89a372878c3cd4a1cd7223abdbd23c3fa75ca22877f7267224)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceStrongSessionAffinityCookie",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "ttl": "ttl"},
)
class ComputeBackendServiceStrongSessionAffinityCookie:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[typing.Union["ComputeBackendServiceStrongSessionAffinityCookieTtl", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#path ComputeBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#ttl ComputeBackendService#ttl}
        '''
        if isinstance(ttl, dict):
            ttl = ComputeBackendServiceStrongSessionAffinityCookieTtl(**ttl)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530f9df067860e1e98f50478433c0d916f62b4cf48a7407bddff583f590cd165)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#name ComputeBackendService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to set for the cookie.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#path ComputeBackendService#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(
        self,
    ) -> typing.Optional["ComputeBackendServiceStrongSessionAffinityCookieTtl"]:
        '''ttl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#ttl ComputeBackendService#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional["ComputeBackendServiceStrongSessionAffinityCookieTtl"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceStrongSessionAffinityCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceStrongSessionAffinityCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceStrongSessionAffinityCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__088f68cd099edfa0c56ea83c3ed02303383f757b19fd6269e14431cbe54610f9)
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#seconds ComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#nanos ComputeBackendService#nanos}
        '''
        value = ComputeBackendServiceStrongSessionAffinityCookieTtl(
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
    ) -> "ComputeBackendServiceStrongSessionAffinityCookieTtlOutputReference":
        return typing.cast("ComputeBackendServiceStrongSessionAffinityCookieTtlOutputReference", jsii.get(self, "ttl"))

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
    ) -> typing.Optional["ComputeBackendServiceStrongSessionAffinityCookieTtl"]:
        return typing.cast(typing.Optional["ComputeBackendServiceStrongSessionAffinityCookieTtl"], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcab261eab2bc38202a3be45b207c50c560b5376efa42509ef2cf4e0192fccbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d40a469f7174b54626d485f0694e32b2ae0c3946ff5077f9a0039fc4e60ae68e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeBackendServiceStrongSessionAffinityCookie]:
        return typing.cast(typing.Optional[ComputeBackendServiceStrongSessionAffinityCookie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceStrongSessionAffinityCookie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10d3cb884077b8812c272cba0f7773797295de544cd4e20964ae6ac73768994e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceStrongSessionAffinityCookieTtl",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeBackendServiceStrongSessionAffinityCookieTtl:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#seconds ComputeBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#nanos ComputeBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b0baca4e66eff62ab4bdf05334739218ef220ebcf694c350997e49a78572397)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#seconds ComputeBackendService#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#nanos ComputeBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceStrongSessionAffinityCookieTtl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceStrongSessionAffinityCookieTtlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceStrongSessionAffinityCookieTtlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a819178230e332c40091cfa46d6d2f6add219b2b9cd43af429fc28f1c3c192f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80755e552cf552de88cd694a3a8890654b02b27871e55cb3dfab8c6f0d42e2e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2467c0c2c1f3acaf295958afcbf6bc5e4d8ebd6a42a693b9cf8acc9ccde31bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeBackendServiceStrongSessionAffinityCookieTtl]:
        return typing.cast(typing.Optional[ComputeBackendServiceStrongSessionAffinityCookieTtl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceStrongSessionAffinityCookieTtl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e3bfe64131d5b844186aa9d4da21ed180ba0ea8aff93d89d2e489365cbc53ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeBackendServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#create ComputeBackendService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#delete ComputeBackendService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#update ComputeBackendService#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b57965453a96bd2cac8c6281ac85a4730f20f5a9b4e0b9606f66c31c039a25a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#create ComputeBackendService#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#delete ComputeBackendService#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#update ComputeBackendService#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16a6a11c0b1d40c5f83aa10000f564e3e3cf925adb20c856a34b28338ab6d6cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b09f28d624209c6cb653d88ac6d3eba35510b5a60a9f85a180182474357d388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e30d79bbdae1de6605015ed16270dcf9fc2dcbf2a19cc01fd47e5add53a6cbc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c01c626f30a67b47da788c282a89db13648c362d0629c86f67c660e2644547ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7901deddfbae94fd8ea8e6372c8d82f16fca574de4eda621cb4bc197e7943a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceTlsSettings",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_config": "authenticationConfig",
        "sni": "sni",
        "subject_alt_names": "subjectAltNames",
    },
)
class ComputeBackendServiceTlsSettings:
    def __init__(
        self,
        *,
        authentication_config: typing.Optional[builtins.str] = None,
        sni: typing.Optional[builtins.str] = None,
        subject_alt_names: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceTlsSettingsSubjectAltNames", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param authentication_config: Reference to the BackendAuthenticationConfig resource from the networksecurity.googleapis.com namespace. Can be used in authenticating TLS connections to the backend, as specified by the authenticationMode field. Can only be specified if authenticationMode is not NONE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#authentication_config ComputeBackendService#authentication_config}
        :param sni: Server Name Indication - see RFC3546 section 3.1. If set, the load balancer sends this string as the SNI hostname in the TLS connection to the backend, and requires that this string match a Subject Alternative Name (SAN) in the backend's server certificate. With a Regional Internet NEG backend, if the SNI is specified here, the load balancer uses it regardless of whether the Regional Internet NEG is specified with FQDN or IP address and port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#sni ComputeBackendService#sni}
        :param subject_alt_names: subject_alt_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#subject_alt_names ComputeBackendService#subject_alt_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e817fc54fa9932597b6ea4eb58029598ffb15f6e445f7497cd101745346ff58d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#authentication_config ComputeBackendService#authentication_config}
        '''
        result = self._values.get("authentication_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sni(self) -> typing.Optional[builtins.str]:
        '''Server Name Indication - see RFC3546 section 3.1. If set, the load balancer sends this string as the SNI hostname in the TLS connection to the backend, and requires that this string match a Subject Alternative Name (SAN) in the backend's server certificate. With a Regional Internet NEG backend, if the SNI is specified here, the load balancer uses it regardless of whether the Regional Internet NEG is specified with FQDN or IP address and port.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#sni ComputeBackendService#sni}
        '''
        result = self._values.get("sni")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_alt_names(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceTlsSettingsSubjectAltNames"]]]:
        '''subject_alt_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#subject_alt_names ComputeBackendService#subject_alt_names}
        '''
        result = self._values.get("subject_alt_names")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceTlsSettingsSubjectAltNames"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceTlsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceTlsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceTlsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e4acede01a8c14258125329fa1168a32ff293858c30398b24f216dbeee8a358)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSubjectAltNames")
    def put_subject_alt_names(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendServiceTlsSettingsSubjectAltNames", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c681546db7b7f7b33fb43e9487f35bc075153111e96f74b89671d6f103c615ca)
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
    ) -> "ComputeBackendServiceTlsSettingsSubjectAltNamesList":
        return typing.cast("ComputeBackendServiceTlsSettingsSubjectAltNamesList", jsii.get(self, "subjectAltNames"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceTlsSettingsSubjectAltNames"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendServiceTlsSettingsSubjectAltNames"]]], jsii.get(self, "subjectAltNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationConfig")
    def authentication_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationConfig"))

    @authentication_config.setter
    def authentication_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e6c34824602f08bb0afb678f6b09d9289415993292c9e0ef011be224008487e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sni")
    def sni(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sni"))

    @sni.setter
    def sni(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31dbc1eda0bae17c2d803b7dcffbee085322b1a06c98ab53127cac8834e512eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sni", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeBackendServiceTlsSettings]:
        return typing.cast(typing.Optional[ComputeBackendServiceTlsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendServiceTlsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a45f76a872f6377121859a21c8fc80421f2b4ddf17c081c464bc907933dc172d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceTlsSettingsSubjectAltNames",
    jsii_struct_bases=[],
    name_mapping={
        "dns_name": "dnsName",
        "uniform_resource_identifier": "uniformResourceIdentifier",
    },
)
class ComputeBackendServiceTlsSettingsSubjectAltNames:
    def __init__(
        self,
        *,
        dns_name: typing.Optional[builtins.str] = None,
        uniform_resource_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dns_name: The SAN specified as a DNS Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#dns_name ComputeBackendService#dns_name}
        :param uniform_resource_identifier: The SAN specified as a URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#uniform_resource_identifier ComputeBackendService#uniform_resource_identifier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a23e4d3af7da654d2e914dae62d7da0d403095b2c1448038642be46d98018746)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#dns_name ComputeBackendService#dns_name}
        '''
        result = self._values.get("dns_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uniform_resource_identifier(self) -> typing.Optional[builtins.str]:
        '''The SAN specified as a URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_service#uniform_resource_identifier ComputeBackendService#uniform_resource_identifier}
        '''
        result = self._values.get("uniform_resource_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendServiceTlsSettingsSubjectAltNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendServiceTlsSettingsSubjectAltNamesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceTlsSettingsSubjectAltNamesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8000f074635beb5cff5ac90d6343f76539046803cfee4174cc3038767fecd9d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeBackendServiceTlsSettingsSubjectAltNamesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a210730b527d5ea4dca716bde1ed981a24d1943d58e18bc5425cbfb226191f6e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeBackendServiceTlsSettingsSubjectAltNamesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489e1d43c0cc7d5989cd44cba370e1f69b8845af13a0271aeba0c1c093f44391)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3484582c2b44095977f9a5e83ef188a6e608a738439ef66b334dbd4f36d4538)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8abcf17849f51bdae7c94239e68d0ec7d434336538c9525ba95fec63c751c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceTlsSettingsSubjectAltNames]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceTlsSettingsSubjectAltNames]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceTlsSettingsSubjectAltNames]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2665356f74295784985177b3ea841c1e7eaae8b7ba5e2659ff3e9327a437244)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendServiceTlsSettingsSubjectAltNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendService.ComputeBackendServiceTlsSettingsSubjectAltNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a666cedc389603f30f168f99f5dc27f036e28a2cae8641c7c46d75144657b386)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdba78cfdcde4778290e239b09f227440de467ad8830d76b42fcafc78708cff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uniformResourceIdentifier")
    def uniform_resource_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uniformResourceIdentifier"))

    @uniform_resource_identifier.setter
    def uniform_resource_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b7226ffbced21cb824e50d911da5ddcd8f50bf07cd7e176dd08140d9e6deeee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uniformResourceIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceTlsSettingsSubjectAltNames]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceTlsSettingsSubjectAltNames]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceTlsSettingsSubjectAltNames]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed7276412c892be971f46a84564ad067ca35e6d8dcb8cfd2e2364eafd09ee69a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeBackendService",
    "ComputeBackendServiceBackend",
    "ComputeBackendServiceBackendCustomMetrics",
    "ComputeBackendServiceBackendCustomMetricsList",
    "ComputeBackendServiceBackendCustomMetricsOutputReference",
    "ComputeBackendServiceBackendList",
    "ComputeBackendServiceBackendOutputReference",
    "ComputeBackendServiceCdnPolicy",
    "ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders",
    "ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersList",
    "ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeadersOutputReference",
    "ComputeBackendServiceCdnPolicyCacheKeyPolicy",
    "ComputeBackendServiceCdnPolicyCacheKeyPolicyOutputReference",
    "ComputeBackendServiceCdnPolicyNegativeCachingPolicy",
    "ComputeBackendServiceCdnPolicyNegativeCachingPolicyList",
    "ComputeBackendServiceCdnPolicyNegativeCachingPolicyOutputReference",
    "ComputeBackendServiceCdnPolicyOutputReference",
    "ComputeBackendServiceCircuitBreakers",
    "ComputeBackendServiceCircuitBreakersOutputReference",
    "ComputeBackendServiceConfig",
    "ComputeBackendServiceConsistentHash",
    "ComputeBackendServiceConsistentHashHttpCookie",
    "ComputeBackendServiceConsistentHashHttpCookieOutputReference",
    "ComputeBackendServiceConsistentHashHttpCookieTtl",
    "ComputeBackendServiceConsistentHashHttpCookieTtlOutputReference",
    "ComputeBackendServiceConsistentHashOutputReference",
    "ComputeBackendServiceCustomMetrics",
    "ComputeBackendServiceCustomMetricsList",
    "ComputeBackendServiceCustomMetricsOutputReference",
    "ComputeBackendServiceIap",
    "ComputeBackendServiceIapOutputReference",
    "ComputeBackendServiceLocalityLbPolicies",
    "ComputeBackendServiceLocalityLbPoliciesCustomPolicy",
    "ComputeBackendServiceLocalityLbPoliciesCustomPolicyOutputReference",
    "ComputeBackendServiceLocalityLbPoliciesList",
    "ComputeBackendServiceLocalityLbPoliciesOutputReference",
    "ComputeBackendServiceLocalityLbPoliciesPolicy",
    "ComputeBackendServiceLocalityLbPoliciesPolicyOutputReference",
    "ComputeBackendServiceLogConfig",
    "ComputeBackendServiceLogConfigOutputReference",
    "ComputeBackendServiceMaxStreamDuration",
    "ComputeBackendServiceMaxStreamDurationOutputReference",
    "ComputeBackendServiceOutlierDetection",
    "ComputeBackendServiceOutlierDetectionBaseEjectionTime",
    "ComputeBackendServiceOutlierDetectionBaseEjectionTimeOutputReference",
    "ComputeBackendServiceOutlierDetectionInterval",
    "ComputeBackendServiceOutlierDetectionIntervalOutputReference",
    "ComputeBackendServiceOutlierDetectionOutputReference",
    "ComputeBackendServiceSecuritySettings",
    "ComputeBackendServiceSecuritySettingsAwsV4Authentication",
    "ComputeBackendServiceSecuritySettingsAwsV4AuthenticationOutputReference",
    "ComputeBackendServiceSecuritySettingsOutputReference",
    "ComputeBackendServiceStrongSessionAffinityCookie",
    "ComputeBackendServiceStrongSessionAffinityCookieOutputReference",
    "ComputeBackendServiceStrongSessionAffinityCookieTtl",
    "ComputeBackendServiceStrongSessionAffinityCookieTtlOutputReference",
    "ComputeBackendServiceTimeouts",
    "ComputeBackendServiceTimeoutsOutputReference",
    "ComputeBackendServiceTlsSettings",
    "ComputeBackendServiceTlsSettingsOutputReference",
    "ComputeBackendServiceTlsSettingsSubjectAltNames",
    "ComputeBackendServiceTlsSettingsSubjectAltNamesList",
    "ComputeBackendServiceTlsSettingsSubjectAltNamesOutputReference",
]

publication.publish()

def _typecheckingstub__ec0ba762c0839c825f34e91e5850dc897bb3c707b681b2a918c2b789e193625e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    affinity_cookie_ttl_sec: typing.Optional[jsii.Number] = None,
    backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cdn_policy: typing.Optional[typing.Union[ComputeBackendServiceCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    circuit_breakers: typing.Optional[typing.Union[ComputeBackendServiceCircuitBreakers, typing.Dict[builtins.str, typing.Any]]] = None,
    compression_mode: typing.Optional[builtins.str] = None,
    connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
    consistent_hash: typing.Optional[typing.Union[ComputeBackendServiceConsistentHash, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceCustomMetrics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_request_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_response_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    edge_security_policy: typing.Optional[builtins.str] = None,
    enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_managed_migration_state: typing.Optional[builtins.str] = None,
    external_managed_migration_testing_percentage: typing.Optional[jsii.Number] = None,
    health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    iap: typing.Optional[typing.Union[ComputeBackendServiceIap, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address_selection_policy: typing.Optional[builtins.str] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    locality_lb_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceLocalityLbPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    locality_lb_policy: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[ComputeBackendServiceLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    max_stream_duration: typing.Optional[typing.Union[ComputeBackendServiceMaxStreamDuration, typing.Dict[builtins.str, typing.Any]]] = None,
    outlier_detection: typing.Optional[typing.Union[ComputeBackendServiceOutlierDetection, typing.Dict[builtins.str, typing.Any]]] = None,
    port_name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    security_policy: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[typing.Union[ComputeBackendServiceSecuritySettings, typing.Dict[builtins.str, typing.Any]]] = None,
    service_lb_policy: typing.Optional[builtins.str] = None,
    session_affinity: typing.Optional[builtins.str] = None,
    strong_session_affinity_cookie: typing.Optional[typing.Union[ComputeBackendServiceStrongSessionAffinityCookie, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeBackendServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_sec: typing.Optional[jsii.Number] = None,
    tls_settings: typing.Optional[typing.Union[ComputeBackendServiceTlsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2748e46a5f1b11fa1ba2271f48b0ee6c968a6e438f5ec3d14c413ca8f3e61aa8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631a5ec1d38f4f75cbb4b6564c6085ff926521acb7ffc779f9427ddbc38dfe74(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ef0aa6cb6aabeed60da75cb71a4342dfca4268b36142979c568209315c2487(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceCustomMetrics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4f78adc1b10b49ad21baa275b9bd5c83c4cdcd7da4e3c6662b0024ad166af58(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceLocalityLbPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96824ed5070e5bc7c1fe7684179435ad257b61c951431ce34b9111ce189e749d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0277052f737abc2533ae00a964194ffd53dfbe7202155760975927d59ab8e078(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9371ee8707a446a33b3e876187c64c99640dc11d0ed107d4bffc83fd9883386c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659607ed2adf1a596de18e4359763d847c01c4652b97fe29de1e1326c45f95ef(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70aa0e8a68885d80c7d14a4f4c4bab18abcccde29f2192536bb33d1228b652e5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc84704b7a4b0151f9470b0aefbca9d96555a281d2905a039f76177a909a4c49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4d43e84f92249c0b68a9ae09de31007c6570a15f3b0c3a6a982676b8bb7120(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb984aefa5d195c2d7b6bbaa9c768a24d1f00fa5a25d25396b5cb063ec6f0b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__943a85e01dce9020e3a0b46ccd264ff8a616b979e64d00017ec3cc7ae337765c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6390a8d6cb61a4ee9828c27a8e78eb83e199a39970cddc7adc3681d04a98f15(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf788042dd6bcd1a9ef797db0560897efba15a0fec845b3330006d80360bb3e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e8c5f4cc9939a8cc198d1601862b423743ea12887ed6bef51560413942c9e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f656c35dca2fa5a40d787284ba916655faed6a5ac132fa04cde7ad5b58ba16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd27edef7e41c782e02d88cf732d20735003608594bdb4c67e9278214cc5179(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07b9cdcb580bc07591873aafb0dc2031115cc12034d85d511a454c09570822f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8548951e1e243230e4d3b0fc8d0a7b7e7a6699b56dddbdc3959aea9e081bac8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8b380663fc71718af8470b0765dc139eabb53e0a08e9cf4b4a97daf5842a84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c93603bc8c05e2929700e323e7049a582ca0d9bba4d8212d44cf2430ecd8ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1ad86e088065fb20fdc2550806001a398faeb243eebb41ab2729e69ad6da9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2397033856c88700a891fd41e8b8279604c2b69b8d243f621ca5d545b21734d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f0801892c026015de994a9cbd6ec9ca0bcdda320dc4d68de0806b2e0e87c0ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083b6be75668e7f751a48bc2e3c41e16d16f0c7d65535be29464a5d66402ac54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014c9f4b87f03952f5215685606fbba530932ac0fbf4e40126e32ef4ecbb2d70(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1712d6d29dcdd70242b1931e30d2669f08eb7cdd6eee53142eda9a5d79ccfce0(
    *,
    group: builtins.str,
    balancing_mode: typing.Optional[builtins.str] = None,
    capacity_scaler: typing.Optional[jsii.Number] = None,
    custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceBackendCustomMetrics, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__0f956c7990787600049c6b19be0d39c889b45954e5c7f063b5b136db3c8fbd6d(
    *,
    dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    max_utilization: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d8d2db6abd80a289e69176073682a1409281312a4c2a864133adc3a638f477(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__065f8bed6797bb1df12d942873aea7e190bc435e4296920df8cbb9b3daa04301(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3cd34ea164c95b4e3fceac427344511254dcc66671651a79aaab18bceebad7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1481940813e8f9e997b96c147b5ae1df8ad68bd457313f52344054156d26a2c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036ba400966c06aa7f211ab1df36f7fb04c4c55885d96bca4b50dd34e3bd8c19(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716ee0f85fd48565484c4d3494880f8c355cac7b8e57f03da634d1e1db742702(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceBackendCustomMetrics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38915529b79bb1bac0b9cc45ea68ec44ccfec379a63c95182ea24a202ad1515f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066d1cb5108ca43617ddb910f8c2877810b22dd9df69ca2808c0f2f0e5d3aa2a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f524b3d11f538d2341a0c460c487e5a37cf8523fe47f3c001aedafcf8dfb0e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633c143a2edd46be950cee2729852a89ed29751307099021f2e8c880808639a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b4bc3750e962831b127285baeb37eb67b606f60e95ea9bfbb73fdfa4195c14(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceBackendCustomMetrics]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f1889fb0fb24811da4e8f71a34e59ae92cbe448d2540403bcc0638491aeabc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8817346a79c3d97c01b769a13ec90fdff2d8c390eba299c5de7d112140b55bd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d6ef3ff4b618d9253593a3de522ca28f5d53a23f49238a9552aca13e83ac6be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196dc0bc639b1cc46f99345f318a3db744656a2e4b04b13ff2abc9fe3b60af49(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e9b3dd22df6082afb15c1087bfa33d2ed75702f42d592d6fd8a80e770d671c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__704d1395eaebe064b4082b10cebaa1de7eb5ad7acea921dfaed612f56c295042(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceBackend]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e257b59166910e01f59db784213cb24af01d5a7656335186a5a2266d210d958(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604ea3a491b0b911e5bd00437a751a561e17d0812ed4721e43db2bd811435926(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceBackendCustomMetrics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2516a4d14ba70a207c45a0513800e2b3422af8233acfaaa292e5c5f871860e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ddc1d98465231a397310c6dd7201eec6fc696341b760aa843247d4c906fc64(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__623c8f1ef6e81db622c7d77dd6f9fe4dc1b7f32b6ef9b2a67b6321e32e71c4f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__877d6ba72963eca51edaae733246f0ecb7712f45d3cd55e448bb7f7c5161399e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1816f5475d20b492516570a55ff5254324360f12b8477c2fdcc2dd6d66b68e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39deb44524038f3dc9f1dc6e1f11531de2c5a5d4d0953af0c317051b001818ac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5702137305f5f9e4b15de1b1e9dc5dcf9676dc20ab9cc62dd8bef63b037703(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638c60ea27b2a232dade2c0bc746d8b338985650df52007540039263cc91f44e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df371e4ebf3da50a4ecbb3817a68cd6f9253b7ccaaf5478fe01267c4b14224e7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0af28b4cff5d6afa26211453ed869914da7bb2f0a17a5a1313c8dd2f97e07e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ed33132efcad8ff0b50bc9b05c794b81328ef510d586e515fa46e20cf1d57a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5debb665558e57788d261a1f03eb2c983b86e3e8273f3f342728ee476bb576(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d945141484f0e78ab3bb08b7beab5069009f63aa5c513451cbc1957354f015(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceBackend]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4aa11413bfd687862b953cafd3548ecf6de4848d4c2b7181b0c3db1af6de753(
    *,
    bypass_cache_on_request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cache_key_policy: typing.Optional[typing.Union[ComputeBackendServiceCdnPolicyCacheKeyPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    cache_mode: typing.Optional[builtins.str] = None,
    client_ttl: typing.Optional[jsii.Number] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    max_ttl: typing.Optional[jsii.Number] = None,
    negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    negative_caching_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceCdnPolicyNegativeCachingPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_coalescing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    serve_while_stale: typing.Optional[jsii.Number] = None,
    signed_url_cache_max_age_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d635107e864305f2ec286c8bafef183b5522d8ac838af18d9ff0a76c38c97f(
    *,
    header_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e43a19bafcdb974380abc4367a5f610e98a5063ff689211c895760ef2253abc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6d033c7291d0bb7e526d5daa98010f42ff8925f0a476c99e99ebccb25a9dd4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ca499ebf4a52baf2d75eb73d54ce71abd6cd2a48a284469e89025699f5b0cb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015289f9133af29e10da36474dd3b775a9a727ec0307ec84a80f271fef9a7fe0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb2ca296e183cc02029ccc8c9aa1590967e6a7df3fa4f40801fb344c1c40ef3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f36b151cc4336707ae4b413751d9bf5a1d7e8c2997e02a31e6fb70a2494ad6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb008bcb1a6622a0d601cee5ce5496f35a4a8ec23bc7f2205f7af011d978eae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7e0430c10110afc99b017097dfae38de9b93fbc629a39f692afbc7385118f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28fe2b9869e13ebea594a0ec2ebf500ed98ab5f2b43c8af004c69482e0f8744b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4b8e187644f2dc323781f3443cd1ef24e4767b558ed8df84498f3b0862e8ae(
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

def _typecheckingstub__bd217cc1b9015265b5f02b01a5167bc5bdcd21d3d541acb095d4976515b8e145(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed81a436bb763aab5d10ef41dbf6b250f40648e6ce535381069049fb1f5d92a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73664ee1221c25d5829c5028b00a367e106c81e2a9aea1cad9650394f42d0a2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69d764bc36e5aec06110dade800e05823238f54ecfaa51832fd80494a0b0ab3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b10dbd15eefa6ffa55c77499b8587bc826ffd273fccc87a9be783fe867361d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff38362765670cf0b4d96792c32207570c072e4030e74cdce09565b8448bf2f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b5221d51574d6d6dbd77b81793c6efb3a34f0e6ba4d70e041af205540d0d03(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f48d994fefd0f29ba6ea30930decb8cc268448b1e973a7426fd268bcdf97ad8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a6e377ab94f4fd6dfa738e7909fdd95912ac0d431f167639fcfa769d55159e(
    value: typing.Optional[ComputeBackendServiceCdnPolicyCacheKeyPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e75de7edcfabb1463e16c83bd3d248dc59b1982fba0d598463dd35be8721193(
    *,
    code: typing.Optional[jsii.Number] = None,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7468b40278131f5eceb36f1547ede5cb4d93ab8196d66df2012971eb77f4d720(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e5dbcfe7d8efda15f2c3387d9cc5c936d1b1dd47a0b76160f5a16bf5df22b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae33597bfad4df6300de5bbb616a28959e30efba6566ccaa0363d5c6ce8b15f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95b76d5c8c8f6bd0ae52c9a0269bb648b9883944d55ac4292128fbb3625b131(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3ad171e897745a023d9e4bcb3647ac1567375dfdbc4c83ae005ee3fbc09134(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40a26c44b5253b4c56057aaca3ad6e09d7a42c0c62c91f66afdcccd303cb7ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCdnPolicyNegativeCachingPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f106b62dc4b14cae11d76079a491a2905b0159bd8a45bace3e3503cffdf496(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32093ae86b56641b7f9b3035ce5e91f2938647a1344c62a2e4a12ca4ebeb844e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee3961a7fc2834fae134d66cdb74b302e850e24f5f9f998dbaeff3ada189008(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961a41302b70499e5465c85b982a832150b19c6c3fc8eca5af9c68eef0c9579c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceCdnPolicyNegativeCachingPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b0b2e545804d6abb22357379cae31ed3769d64911f7781dcc58237e18fce0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d327e2eac71b95b8971702bd79146a9582c730cf2f76afc1de5ef46b166cb0b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceCdnPolicyBypassCacheOnRequestHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762feef19670ce9239d545e3c3e8d13399966ce5122ac9c312a609cb3b30f394(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceCdnPolicyNegativeCachingPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac16ac0af5022071fbe022094565931b2903aeeb88330294962424efcf99dde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8671ae97b71554ef457e726ac4770ec63a27c9a724235ba76a9649c0fb1606(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eb811b573498d4705c4d804bd3b545a031df2fc26984c5d6824cf36cdefd60d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e017bc59c556a2f13f4f44350f919e2d123d47451ab638504a3c4d0152af7f25(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417e062007cbf6d45935cd042e7c3c971a6b0dc3311ba72b647e2eba6b7aba4f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d97c35b6cc6d794e29b95c0f954a1b5a48b026d2b67671301ab68cc5b4e2aca7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7212cca2bec89b9d39cdb9324eaaa4ac3a04e0c5f84c4066892d7391a05ebc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb995bbea02eda253769b8533cc37492371c20b35eca24012b750e5f633335a5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493125191f9c980a5540244693e0987f4c01a24133cddf4dc00cfff1027faa3b(
    value: typing.Optional[ComputeBackendServiceCdnPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cabb5dd50ebcf417ca6d890e8eabad68602526db561901f7904f994168fe8b2f(
    *,
    max_connections: typing.Optional[jsii.Number] = None,
    max_pending_requests: typing.Optional[jsii.Number] = None,
    max_requests: typing.Optional[jsii.Number] = None,
    max_requests_per_connection: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1f4aadcbd8d97c0ae65c4ae65f1f6a5a3cc16749d2c4c1eeb4948118ac5d62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1a9dc1a125e18fa78b09da195dfbcb8108bf90c518568c70c2ba06032a1101(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046c38d353eb17c495b3615bab450e7a5e6e7f984310a32d396fd789ffd0923d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d003517abd224c1aa133a618eda57fcb5ca7fd287b43598afc3ad1b6d63f3e61(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2f102e717387f1df42d2235cebdf1a7a16ec13aafbd43c7e2e6f42c7e7fefd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa95b5e7795cc254ad79205ff211bb4f7454c756e1656edcacc178c2c5f8257(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e6e0dccbc322916e5e2fe1426b9a099501fa355739dc0e62be5c2ced20855f(
    value: typing.Optional[ComputeBackendServiceCircuitBreakers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cdf2349083c2692c68d52e8aef7e24451d6ac647ece4b93819a2c462dedcbcc(
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
    backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cdn_policy: typing.Optional[typing.Union[ComputeBackendServiceCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    circuit_breakers: typing.Optional[typing.Union[ComputeBackendServiceCircuitBreakers, typing.Dict[builtins.str, typing.Any]]] = None,
    compression_mode: typing.Optional[builtins.str] = None,
    connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
    consistent_hash: typing.Optional[typing.Union[ComputeBackendServiceConsistentHash, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceCustomMetrics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_request_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_response_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    edge_security_policy: typing.Optional[builtins.str] = None,
    enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_managed_migration_state: typing.Optional[builtins.str] = None,
    external_managed_migration_testing_percentage: typing.Optional[jsii.Number] = None,
    health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    iap: typing.Optional[typing.Union[ComputeBackendServiceIap, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address_selection_policy: typing.Optional[builtins.str] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    locality_lb_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceLocalityLbPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    locality_lb_policy: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[ComputeBackendServiceLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    max_stream_duration: typing.Optional[typing.Union[ComputeBackendServiceMaxStreamDuration, typing.Dict[builtins.str, typing.Any]]] = None,
    outlier_detection: typing.Optional[typing.Union[ComputeBackendServiceOutlierDetection, typing.Dict[builtins.str, typing.Any]]] = None,
    port_name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    security_policy: typing.Optional[builtins.str] = None,
    security_settings: typing.Optional[typing.Union[ComputeBackendServiceSecuritySettings, typing.Dict[builtins.str, typing.Any]]] = None,
    service_lb_policy: typing.Optional[builtins.str] = None,
    session_affinity: typing.Optional[builtins.str] = None,
    strong_session_affinity_cookie: typing.Optional[typing.Union[ComputeBackendServiceStrongSessionAffinityCookie, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeBackendServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_sec: typing.Optional[jsii.Number] = None,
    tls_settings: typing.Optional[typing.Union[ComputeBackendServiceTlsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24249d474b94c3417b540849d329bc41c585129641ce6113b30c323aa69413d3(
    *,
    http_cookie: typing.Optional[typing.Union[ComputeBackendServiceConsistentHashHttpCookie, typing.Dict[builtins.str, typing.Any]]] = None,
    http_header_name: typing.Optional[builtins.str] = None,
    minimum_ring_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5768d1136f62b838c574b16145c7188201288dafb98c03e5578ceb10e2337561(
    *,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[typing.Union[ComputeBackendServiceConsistentHashHttpCookieTtl, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dc9a69f0721dcf414346aa584cf38f51237774dee2cc229063c568e860b6047(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b6129fd0530717d7336d4da91f11dfe51cd66bc046d526a65e35e475e185e05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7152ac7f26e0caadc237699d96122fd12f8a17f89460ad3fd259d58ccf21f607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1afc370d2255683a0cec6e2b9515ad8d3240fbb49f0d5cf2fdc4de57f7fe3404(
    value: typing.Optional[ComputeBackendServiceConsistentHashHttpCookie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cfcf0c79c0d13aa2f67b889ee04395156d17df1d9e0babfc3e4deef93b23770(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c8b8be840be8b0f5a21e055c712ab5850d9b290075406082badd5c426689a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e932d49ab438f3da6fcece89f6db9fcd10bf8df83f528fd6c95ab38cc5099c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7a1e22dc98a1d55244cb1347812bfd6f6c58a1316594f41888c9d93231331f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7773f8dd09c4d1b66a0fb03e8536572a02ed9ebaf6a1791616bf75f737ae0f26(
    value: typing.Optional[ComputeBackendServiceConsistentHashHttpCookieTtl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fb90af6a3f12a1a032cd8344bc6ac7ad2437cfe63ff782cf6ad42bc96f0f73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc7608d0727dcf8af90febc6a547d6630dadfdcb3e67429be98139cb06067ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b99cb7a514f000754cc3b912d8a88fe4ea59aa8fef20de3cec7826ee1140a8c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f50b2e209cf84d1bcb9963bbaea103840c94627ccd23e75cd11cea81fc0a9cc(
    value: typing.Optional[ComputeBackendServiceConsistentHash],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f72eae0a6616c2645a2bf67b5e7ad93c83ea1dc172e67318108bd88c5768b90(
    *,
    dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd241ee729fe74f60c9b8d9b40375fbb7cdb3fed5dc50e8cdbdb472a371dd6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f7d5529c8ab1992e0c9aa4c00affa1ae844ec57c31e8e1b3ca2878329e74543(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ed245cdf2cb4f2e9ec9b786694bd97a26722b0bf9671f8da3dbb33365c2c43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9104840a743b8ff0172d046d1da375c9e6c2ee8ffcb0ef2f5c2b754768ac17e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470202cdc8867572b7f9e9af73d0578fcb8ea91e5bc0c2919ee849913a078d92(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7622d1db5f82075877a1e4649c2f6bf9d1ddca4670bbe1135b4d3522893dbec8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceCustomMetrics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160f8b263ab2dbea0b4178319f661b6a6e3afaff421517a3d9a58d48e929b6be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b464bedf82720fd7fbf9318e8d0b55b3f466960519c1518eb79da6eabe420cd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a3dd17be65a5e6ccc995acaf7d41728a2694839023df512011deefecf4765b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7e19c08710afac8058116876f0b96bae4d5bb80e8761132ade854808c445845(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceCustomMetrics]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db6a067a9c2bb1e490175d2888e307496906618b95fd5aaf9f8986908ed6a63(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    oauth2_client_id: typing.Optional[builtins.str] = None,
    oauth2_client_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abded96dff214f1d51b58ff01b54751f2bba1ef36785b96d14140d4cc2b4af3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ea67c9f0e091e51c97a0921de7eb5c7ce85853d368855bec0ec7f2fedaa8ab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2daa88fdf2922ef32100c14a14547f8b2df605964a354cc274130f590ae2d2a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b53be0989d8177aff045165d8112e47fb1bc0d95d1062e33a998fb756632f85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c22502ece2e3bec3c41b02c6a50f4f861fd6c92bb78f6806986a79b5ed180bf9(
    value: typing.Optional[ComputeBackendServiceIap],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__133b9c63a29d398d55f5e8aa6d1e3436d6cde27a2e9e345f7cf0094105fdf2e7(
    *,
    custom_policy: typing.Optional[typing.Union[ComputeBackendServiceLocalityLbPoliciesCustomPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    policy: typing.Optional[typing.Union[ComputeBackendServiceLocalityLbPoliciesPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a181450b18a2ff77a72f97f47cba6f914360aeaa61388eb73dd3670239fad8(
    *,
    name: builtins.str,
    data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153b2c3cd822a8ba70a6135036a50c4bc23bd0e55b4b4a0110cc0568f5c7b380(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d38e3b6c8a27e09b83f8a509690ea0460cfeb35369f51eaa5934d6a9842f8bd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b537cb6cf6fa652c76c374b0c9fca7a4e8eb3d1c4fafd294b8cc12dd001d196d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f16611013386bb50dc0f5ad76f228b3aa080a48261f12673179be1b649d6767(
    value: typing.Optional[ComputeBackendServiceLocalityLbPoliciesCustomPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4f5dcb2702ce35c18a835f83a1ba36275af06539f75cf783f2130d1e11cd28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ff33eb1c2c47ef399616f912d2b56a382bea2a265a0f380d1d8856ebe1fa44(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df52b34431c2035337c295e686bf27801fc9d3a87e9b0f5710bbf1bce6d0ac94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2913986f2e4889fb96ef60840c6db5eec594b07c093f6edc1838fca6a00303d7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2887e2527250450f62fbe796870e84cf7cebec946473baa844b9971c7f1237d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ba32ebb1c0dedd3033d22e1fc94c33164e322c3d7a15f50369826eea8092e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceLocalityLbPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349563c70352b761154e31a1fa0a9745846386dbfec2b51edc5b083e6f5fe641(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976e1bf01e8c4c7241575ae7e460d2671175995d73a83293c4d56024abb7ad11(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceLocalityLbPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2a96fb847d7ef407f55e7fd8c058cfa85c50497de5475c94ee8c1df0592ea1(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5f1182a2241adb700a51d3217e3a5d00c80eaaa0b7f63c02c858a2d383190a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a30b0b63005c8f1d6582949fc38e5ece28c9349400f012d4d9222c39eb6e50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e3f918bea2e83a5679077d4c61d9116818042031f9d3f34042d893c2a63a33(
    value: typing.Optional[ComputeBackendServiceLocalityLbPoliciesPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99b387fa30cf77c6d12fba5a600b2b14d0e573d800567f0c9fec0fe7280d0ab8(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    optional_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    optional_mode: typing.Optional[builtins.str] = None,
    sample_rate: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519f8a5f09ccbf1f31b71ec1052c98a84a673f49d9dd31c17c8c157cbcda76cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3ac8736b55b88237f7a5d9f52ec5dc98c3dbf3d26c51dacc9c6a0bce82f577(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8428bfb9a93c42eae890039a7452f56da7c195d1e7b2af8c1f420d119954dfd1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e9a371cc45970994928b6baadb48324cb38061405666c3c1adef76f1d6ec39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a0a0b451fa7e0a5df9ea96341586659540e7512c4adf7685a2af38755bbb50(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2bd8556fed1a7aacebe1feb97fcefe1e6f62e5af4be5d1a36aa3bac171187c(
    value: typing.Optional[ComputeBackendServiceLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6210bab88f06770c9a44434e10ca3c48da4072e02de6effe4d309353f56ce161(
    *,
    seconds: builtins.str,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85cb9cb82159a00e840111ffa210a705deebe1bee6a403d6fc65203bfe1836bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d3f5de690679adee476e35ff0f759efa983b4355c8edea0996f3880a0514ff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8fe3b7074dc52c4068aa2399407fe8a71d0e9f9babd577988eed62da323602b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353f8f4466a866472d52c6733c4ba623730f62cabfe389007797e204c9d35c10(
    value: typing.Optional[ComputeBackendServiceMaxStreamDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c3d24e022e54b5a59882f6b33ab107c28418b401ee4a0357f8fc66c41b2cb3(
    *,
    base_ejection_time: typing.Optional[typing.Union[ComputeBackendServiceOutlierDetectionBaseEjectionTime, typing.Dict[builtins.str, typing.Any]]] = None,
    consecutive_errors: typing.Optional[jsii.Number] = None,
    consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
    enforcing_consecutive_errors: typing.Optional[jsii.Number] = None,
    enforcing_consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
    enforcing_success_rate: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[typing.Union[ComputeBackendServiceOutlierDetectionInterval, typing.Dict[builtins.str, typing.Any]]] = None,
    max_ejection_percent: typing.Optional[jsii.Number] = None,
    success_rate_minimum_hosts: typing.Optional[jsii.Number] = None,
    success_rate_request_volume: typing.Optional[jsii.Number] = None,
    success_rate_stdev_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3662efd40c09f95427a97d2217dcc0b97b81d63422d2b868ebb9075becba9260(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b177162f774fd4730a19210b219bad426dcff46192144fefd0c786f1ab8268(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39ecef76a7fae9622c29aa19a03ec1b816a05306ed1e7f29b69de3da62924f35(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccce62b190a3b654b4765c9dbc5a232713c2d31be90cc91908cb2ac32c4d86e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b56ab9820d66f5e91a2aecf74b94d38038eab423878bc48cf5d3c0607c154960(
    value: typing.Optional[ComputeBackendServiceOutlierDetectionBaseEjectionTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd1d0c3b6bf832794859f2f7f9d7061de4d49f22cad232db8b386a825c7347b(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f4c5f0af97292ee12a9e45b60b6de1de7660defea3d9a37829d07b0c2efb15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81230bfc5b088b7c9795bf85651cef7f0b69a45592828219d328556c13b18e6f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee116e28f96f3106bf14cf5bbbfc23d1a423b98cebe86646a7e4485cdfc46eac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9460cbf2049c96fd7f500b8274ad2363d109c2aa4c984bbfd175bc82b997c184(
    value: typing.Optional[ComputeBackendServiceOutlierDetectionInterval],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e335509fc6272d824948829d1d640d984b69a2c28b9393e42b78f2ab2af0609(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8c05522ede1dd5530975f838dd85f01e8bbfc6a816e28b45802d14da5d6d0c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23aa1be1239d5feff22cf92795a1e0507c34fe46be7024273703ccea8f93c24(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86ab261cdc33bb4554de4c273bbb25e20ddc2fba7b45014c52de9fdf1f2c26a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ed83fb6e7cc5f1f243d93a1f6426cf2e6e392f5ca81f59a8e125e92abda1b1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41dc4c1caefb84069ed0e71e47dea86aaa83ee22a67a709e2860c3eee7d2719b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc717166afb5409882f4daf3e596592720c1aefafec6b1ae546acd8f29d8c3c1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0aec2735d2942ceef833f71ef98561dd586063ce35ef677cdc36d47b27917b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fe617d93252699eddf26326c8d987a9494aac421c8fc82a680086b4ad9030e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7251c000500ede829be00f87ae8adac21d1c429dea6d97a395c46a8ba57361d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__012559c26bbac5595967249d0084d85184c63347dde6fd8e9d5a5bcdcbb13e1f(
    value: typing.Optional[ComputeBackendServiceOutlierDetection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd617f036e6ba15b8492ca68c20a028b6c7af7395253176e59bc7f135ecb6b3(
    *,
    aws_v4_authentication: typing.Optional[typing.Union[ComputeBackendServiceSecuritySettingsAwsV4Authentication, typing.Dict[builtins.str, typing.Any]]] = None,
    client_tls_policy: typing.Optional[builtins.str] = None,
    subject_alt_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81791ca30ad8b119b0c9aa936cf81fbc3af5d157dd93b84c9d7bd38d7ad29cac(
    *,
    access_key: typing.Optional[builtins.str] = None,
    access_key_id: typing.Optional[builtins.str] = None,
    access_key_version: typing.Optional[builtins.str] = None,
    origin_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56246216e26ae82b24579db5ad149d50faee9d434b6770bca15c610dc1cd5828(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4609b7312c0e5067c24b9be19ec7b28748aeb92d16ef85df5a5e32091c94706e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395b36b6595f2680d5b9a9bd007ef63e876ef9862c65794a6b7386e710023be4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975f888eb54839b2b82234e03dc73f267458965d186a50c5761c814b10529199(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f3c5a1e550cddc802001ad627b99a7bdf7e875f2edee7b99cf17ef3a03f86f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9caef7639dd8cb7bd6017cf5375450bc5ba1d00690627b4456b543efe17970d(
    value: typing.Optional[ComputeBackendServiceSecuritySettingsAwsV4Authentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91215240621f88f545852d5ce74e966883722e7653c3ce2a3c53d9d903f39ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f3e1fa8dba24294768465ee0250a147c835080cd21deda3358bcecab7a0a9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b046c1b0cae4789203d72db60d141646b4775ef6f24f0a947c4f57d7068bf78a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d84cb2cb1a53da89a372878c3cd4a1cd7223abdbd23c3fa75ca22877f7267224(
    value: typing.Optional[ComputeBackendServiceSecuritySettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530f9df067860e1e98f50478433c0d916f62b4cf48a7407bddff583f590cd165(
    *,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[typing.Union[ComputeBackendServiceStrongSessionAffinityCookieTtl, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088f68cd099edfa0c56ea83c3ed02303383f757b19fd6269e14431cbe54610f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcab261eab2bc38202a3be45b207c50c560b5376efa42509ef2cf4e0192fccbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40a469f7174b54626d485f0694e32b2ae0c3946ff5077f9a0039fc4e60ae68e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d3cb884077b8812c272cba0f7773797295de544cd4e20964ae6ac73768994e(
    value: typing.Optional[ComputeBackendServiceStrongSessionAffinityCookie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0baca4e66eff62ab4bdf05334739218ef220ebcf694c350997e49a78572397(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a819178230e332c40091cfa46d6d2f6add219b2b9cd43af429fc28f1c3c192f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80755e552cf552de88cd694a3a8890654b02b27871e55cb3dfab8c6f0d42e2e8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2467c0c2c1f3acaf295958afcbf6bc5e4d8ebd6a42a693b9cf8acc9ccde31bc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e3bfe64131d5b844186aa9d4da21ed180ba0ea8aff93d89d2e489365cbc53ac(
    value: typing.Optional[ComputeBackendServiceStrongSessionAffinityCookieTtl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b57965453a96bd2cac8c6281ac85a4730f20f5a9b4e0b9606f66c31c039a25a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a6a11c0b1d40c5f83aa10000f564e3e3cf925adb20c856a34b28338ab6d6cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b09f28d624209c6cb653d88ac6d3eba35510b5a60a9f85a180182474357d388(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30d79bbdae1de6605015ed16270dcf9fc2dcbf2a19cc01fd47e5add53a6cbc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01c626f30a67b47da788c282a89db13648c362d0629c86f67c660e2644547ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7901deddfbae94fd8ea8e6372c8d82f16fca574de4eda621cb4bc197e7943a6d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e817fc54fa9932597b6ea4eb58029598ffb15f6e445f7497cd101745346ff58d(
    *,
    authentication_config: typing.Optional[builtins.str] = None,
    sni: typing.Optional[builtins.str] = None,
    subject_alt_names: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceTlsSettingsSubjectAltNames, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4acede01a8c14258125329fa1168a32ff293858c30398b24f216dbeee8a358(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c681546db7b7f7b33fb43e9487f35bc075153111e96f74b89671d6f103c615ca(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendServiceTlsSettingsSubjectAltNames, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e6c34824602f08bb0afb678f6b09d9289415993292c9e0ef011be224008487e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31dbc1eda0bae17c2d803b7dcffbee085322b1a06c98ab53127cac8834e512eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45f76a872f6377121859a21c8fc80421f2b4ddf17c081c464bc907933dc172d(
    value: typing.Optional[ComputeBackendServiceTlsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23e4d3af7da654d2e914dae62d7da0d403095b2c1448038642be46d98018746(
    *,
    dns_name: typing.Optional[builtins.str] = None,
    uniform_resource_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8000f074635beb5cff5ac90d6343f76539046803cfee4174cc3038767fecd9d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a210730b527d5ea4dca716bde1ed981a24d1943d58e18bc5425cbfb226191f6e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489e1d43c0cc7d5989cd44cba370e1f69b8845af13a0271aeba0c1c093f44391(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3484582c2b44095977f9a5e83ef188a6e608a738439ef66b334dbd4f36d4538(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8abcf17849f51bdae7c94239e68d0ec7d434336538c9525ba95fec63c751c86(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2665356f74295784985177b3ea841c1e7eaae8b7ba5e2659ff3e9327a437244(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendServiceTlsSettingsSubjectAltNames]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a666cedc389603f30f168f99f5dc27f036e28a2cae8641c7c46d75144657b386(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdba78cfdcde4778290e239b09f227440de467ad8830d76b42fcafc78708cff1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7226ffbced21cb824e50d911da5ddcd8f50bf07cd7e176dd08140d9e6deeee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7276412c892be971f46a84564ad067ca35e6d8dcb8cfd2e2364eafd09ee69a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendServiceTlsSettingsSubjectAltNames]],
) -> None:
    """Type checking stubs"""
    pass
