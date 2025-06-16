r'''
# `google_compute_region_health_check`

Refer to the Terraform Registry for docs: [`google_compute_region_health_check`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check).
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


class GoogleComputeRegionHealthCheck(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheck",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check google_compute_region_health_check}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        check_interval_sec: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        grpc_health_check: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckGrpcHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_tls_health_check: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckGrpcTlsHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        healthy_threshold: typing.Optional[jsii.Number] = None,
        http2_health_check: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckHttp2HealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        http_health_check: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckHttpHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        https_health_check: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckHttpsHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        ssl_health_check: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckSslHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        tcp_health_check: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckTcpHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_sec: typing.Optional[jsii.Number] = None,
        unhealthy_threshold: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check google_compute_region_health_check} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#name GoogleComputeRegionHealthCheck#name}
        :param check_interval_sec: How often (in seconds) to send a health check. The default value is 5 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#check_interval_sec GoogleComputeRegionHealthCheck#check_interval_sec}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#description GoogleComputeRegionHealthCheck#description}
        :param grpc_health_check: grpc_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#grpc_health_check GoogleComputeRegionHealthCheck#grpc_health_check}
        :param grpc_tls_health_check: grpc_tls_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#grpc_tls_health_check GoogleComputeRegionHealthCheck#grpc_tls_health_check}
        :param healthy_threshold: A so-far unhealthy instance will be marked healthy after this many consecutive successes. The default value is 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#healthy_threshold GoogleComputeRegionHealthCheck#healthy_threshold}
        :param http2_health_check: http2_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#http2_health_check GoogleComputeRegionHealthCheck#http2_health_check}
        :param http_health_check: http_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#http_health_check GoogleComputeRegionHealthCheck#http_health_check}
        :param https_health_check: https_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#https_health_check GoogleComputeRegionHealthCheck#https_health_check}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#id GoogleComputeRegionHealthCheck#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#log_config GoogleComputeRegionHealthCheck#log_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#project GoogleComputeRegionHealthCheck#project}.
        :param region: The Region in which the created health check should reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#region GoogleComputeRegionHealthCheck#region}
        :param ssl_health_check: ssl_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#ssl_health_check GoogleComputeRegionHealthCheck#ssl_health_check}
        :param tcp_health_check: tcp_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#tcp_health_check GoogleComputeRegionHealthCheck#tcp_health_check}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#timeouts GoogleComputeRegionHealthCheck#timeouts}
        :param timeout_sec: How long (in seconds) to wait before claiming failure. The default value is 5 seconds. It is invalid for timeoutSec to have greater value than checkIntervalSec. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#timeout_sec GoogleComputeRegionHealthCheck#timeout_sec}
        :param unhealthy_threshold: A so-far healthy instance will be marked unhealthy after this many consecutive failures. The default value is 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#unhealthy_threshold GoogleComputeRegionHealthCheck#unhealthy_threshold}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc3e4120bbbab4f16f445b03fe771b23ad48b3bc355fadb5379c538901d442a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeRegionHealthCheckConfig(
            name=name,
            check_interval_sec=check_interval_sec,
            description=description,
            grpc_health_check=grpc_health_check,
            grpc_tls_health_check=grpc_tls_health_check,
            healthy_threshold=healthy_threshold,
            http2_health_check=http2_health_check,
            http_health_check=http_health_check,
            https_health_check=https_health_check,
            id=id,
            log_config=log_config,
            project=project,
            region=region,
            ssl_health_check=ssl_health_check,
            tcp_health_check=tcp_health_check,
            timeouts=timeouts,
            timeout_sec=timeout_sec,
            unhealthy_threshold=unhealthy_threshold,
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
        '''Generates CDKTF code for importing a GoogleComputeRegionHealthCheck resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeRegionHealthCheck to import.
        :param import_from_id: The id of the existing GoogleComputeRegionHealthCheck that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeRegionHealthCheck to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f46ef04a3182679c9fd2f467182ebea1a74b390768e9968e1f1a0356d69bc85)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putGrpcHealthCheck")
    def put_grpc_health_check(
        self,
        *,
        grpc_service_name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        port_name: typing.Optional[builtins.str] = None,
        port_specification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param grpc_service_name: The gRPC service name for the health check. The value of grpcServiceName has the following meanings by convention:. - Empty serviceName means the overall status of all services at the backend. - Non-empty serviceName means the health of that gRPC service, as defined by the owner of the service. The grpcServiceName can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#grpc_service_name GoogleComputeRegionHealthCheck#grpc_service_name}
        :param port: The port number for the health check request. Must be specified if portName and portSpecification are not set or if port_specification is USE_FIXED_PORT. Valid values are 1 through 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, gRPC health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        '''
        value = GoogleComputeRegionHealthCheckGrpcHealthCheck(
            grpc_service_name=grpc_service_name,
            port=port,
            port_name=port_name,
            port_specification=port_specification,
        )

        return typing.cast(None, jsii.invoke(self, "putGrpcHealthCheck", [value]))

    @jsii.member(jsii_name="putGrpcTlsHealthCheck")
    def put_grpc_tls_health_check(
        self,
        *,
        grpc_service_name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        port_specification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param grpc_service_name: The gRPC service name for the health check. The value of grpcServiceName has the following meanings by convention:. - Empty serviceName means the overall status of all services at the backend. - Non-empty serviceName means the health of that gRPC service, as defined by the owner of the service. The grpcServiceName can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#grpc_service_name GoogleComputeRegionHealthCheck#grpc_service_name}
        :param port: The port number for the health check request. Must be specified if port_specification is USE_FIXED_PORT. Valid values are 1 through 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': Not supported for GRPC with TLS health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, gRPC health check follows behavior specified in the 'port' field. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        '''
        value = GoogleComputeRegionHealthCheckGrpcTlsHealthCheck(
            grpc_service_name=grpc_service_name,
            port=port,
            port_specification=port_specification,
        )

        return typing.cast(None, jsii.invoke(self, "putGrpcTlsHealthCheck", [value]))

    @jsii.member(jsii_name="putHttp2HealthCheck")
    def put_http2_health_check(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        port_name: typing.Optional[builtins.str] = None,
        port_specification: typing.Optional[builtins.str] = None,
        proxy_header: typing.Optional[builtins.str] = None,
        request_path: typing.Optional[builtins.str] = None,
        response: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: The value of the host header in the HTTP2 health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#host GoogleComputeRegionHealthCheck#host}
        :param port: The TCP port number for the HTTP2 health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTP2 health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#proxy_header GoogleComputeRegionHealthCheck#proxy_header}
        :param request_path: The request path of the HTTP2 health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#request_path GoogleComputeRegionHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#response GoogleComputeRegionHealthCheck#response}
        '''
        value = GoogleComputeRegionHealthCheckHttp2HealthCheck(
            host=host,
            port=port,
            port_name=port_name,
            port_specification=port_specification,
            proxy_header=proxy_header,
            request_path=request_path,
            response=response,
        )

        return typing.cast(None, jsii.invoke(self, "putHttp2HealthCheck", [value]))

    @jsii.member(jsii_name="putHttpHealthCheck")
    def put_http_health_check(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        port_name: typing.Optional[builtins.str] = None,
        port_specification: typing.Optional[builtins.str] = None,
        proxy_header: typing.Optional[builtins.str] = None,
        request_path: typing.Optional[builtins.str] = None,
        response: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: The value of the host header in the HTTP health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#host GoogleComputeRegionHealthCheck#host}
        :param port: The TCP port number for the HTTP health check request. The default value is 80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTP health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#proxy_header GoogleComputeRegionHealthCheck#proxy_header}
        :param request_path: The request path of the HTTP health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#request_path GoogleComputeRegionHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#response GoogleComputeRegionHealthCheck#response}
        '''
        value = GoogleComputeRegionHealthCheckHttpHealthCheck(
            host=host,
            port=port,
            port_name=port_name,
            port_specification=port_specification,
            proxy_header=proxy_header,
            request_path=request_path,
            response=response,
        )

        return typing.cast(None, jsii.invoke(self, "putHttpHealthCheck", [value]))

    @jsii.member(jsii_name="putHttpsHealthCheck")
    def put_https_health_check(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        port_name: typing.Optional[builtins.str] = None,
        port_specification: typing.Optional[builtins.str] = None,
        proxy_header: typing.Optional[builtins.str] = None,
        request_path: typing.Optional[builtins.str] = None,
        response: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: The value of the host header in the HTTPS health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#host GoogleComputeRegionHealthCheck#host}
        :param port: The TCP port number for the HTTPS health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTPS health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#proxy_header GoogleComputeRegionHealthCheck#proxy_header}
        :param request_path: The request path of the HTTPS health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#request_path GoogleComputeRegionHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#response GoogleComputeRegionHealthCheck#response}
        '''
        value = GoogleComputeRegionHealthCheckHttpsHealthCheck(
            host=host,
            port=port,
            port_name=port_name,
            port_specification=port_specification,
            proxy_header=proxy_header,
            request_path=request_path,
            response=response,
        )

        return typing.cast(None, jsii.invoke(self, "putHttpsHealthCheck", [value]))

    @jsii.member(jsii_name="putLogConfig")
    def put_log_config(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable: Indicates whether or not to export logs. This is false by default, which means no health check logging will be done. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#enable GoogleComputeRegionHealthCheck#enable}
        '''
        value = GoogleComputeRegionHealthCheckLogConfig(enable=enable)

        return typing.cast(None, jsii.invoke(self, "putLogConfig", [value]))

    @jsii.member(jsii_name="putSslHealthCheck")
    def put_ssl_health_check(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        port_name: typing.Optional[builtins.str] = None,
        port_specification: typing.Optional[builtins.str] = None,
        proxy_header: typing.Optional[builtins.str] = None,
        request: typing.Optional[builtins.str] = None,
        response: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: The TCP port number for the SSL health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, SSL health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#proxy_header GoogleComputeRegionHealthCheck#proxy_header}
        :param request: The application data to send once the SSL connection has been established (default value is empty). If both request and response are empty, the connection establishment alone will indicate health. The request data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#request GoogleComputeRegionHealthCheck#request}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#response GoogleComputeRegionHealthCheck#response}
        '''
        value = GoogleComputeRegionHealthCheckSslHealthCheck(
            port=port,
            port_name=port_name,
            port_specification=port_specification,
            proxy_header=proxy_header,
            request=request,
            response=response,
        )

        return typing.cast(None, jsii.invoke(self, "putSslHealthCheck", [value]))

    @jsii.member(jsii_name="putTcpHealthCheck")
    def put_tcp_health_check(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        port_name: typing.Optional[builtins.str] = None,
        port_specification: typing.Optional[builtins.str] = None,
        proxy_header: typing.Optional[builtins.str] = None,
        request: typing.Optional[builtins.str] = None,
        response: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: The TCP port number for the TCP health check request. The default value is 80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, TCP health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#proxy_header GoogleComputeRegionHealthCheck#proxy_header}
        :param request: The application data to send once the TCP connection has been established (default value is empty). If both request and response are empty, the connection establishment alone will indicate health. The request data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#request GoogleComputeRegionHealthCheck#request}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#response GoogleComputeRegionHealthCheck#response}
        '''
        value = GoogleComputeRegionHealthCheckTcpHealthCheck(
            port=port,
            port_name=port_name,
            port_specification=port_specification,
            proxy_header=proxy_header,
            request=request,
            response=response,
        )

        return typing.cast(None, jsii.invoke(self, "putTcpHealthCheck", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#create GoogleComputeRegionHealthCheck#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#delete GoogleComputeRegionHealthCheck#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#update GoogleComputeRegionHealthCheck#update}.
        '''
        value = GoogleComputeRegionHealthCheckTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCheckIntervalSec")
    def reset_check_interval_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckIntervalSec", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetGrpcHealthCheck")
    def reset_grpc_health_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpcHealthCheck", []))

    @jsii.member(jsii_name="resetGrpcTlsHealthCheck")
    def reset_grpc_tls_health_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpcTlsHealthCheck", []))

    @jsii.member(jsii_name="resetHealthyThreshold")
    def reset_healthy_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthyThreshold", []))

    @jsii.member(jsii_name="resetHttp2HealthCheck")
    def reset_http2_health_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp2HealthCheck", []))

    @jsii.member(jsii_name="resetHttpHealthCheck")
    def reset_http_health_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHealthCheck", []))

    @jsii.member(jsii_name="resetHttpsHealthCheck")
    def reset_https_health_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsHealthCheck", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogConfig")
    def reset_log_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSslHealthCheck")
    def reset_ssl_health_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslHealthCheck", []))

    @jsii.member(jsii_name="resetTcpHealthCheck")
    def reset_tcp_health_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpHealthCheck", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimeoutSec")
    def reset_timeout_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSec", []))

    @jsii.member(jsii_name="resetUnhealthyThreshold")
    def reset_unhealthy_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnhealthyThreshold", []))

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
    @jsii.member(jsii_name="grpcHealthCheck")
    def grpc_health_check(
        self,
    ) -> "GoogleComputeRegionHealthCheckGrpcHealthCheckOutputReference":
        return typing.cast("GoogleComputeRegionHealthCheckGrpcHealthCheckOutputReference", jsii.get(self, "grpcHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="grpcTlsHealthCheck")
    def grpc_tls_health_check(
        self,
    ) -> "GoogleComputeRegionHealthCheckGrpcTlsHealthCheckOutputReference":
        return typing.cast("GoogleComputeRegionHealthCheckGrpcTlsHealthCheckOutputReference", jsii.get(self, "grpcTlsHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckId")
    def health_check_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthCheckId"))

    @builtins.property
    @jsii.member(jsii_name="http2HealthCheck")
    def http2_health_check(
        self,
    ) -> "GoogleComputeRegionHealthCheckHttp2HealthCheckOutputReference":
        return typing.cast("GoogleComputeRegionHealthCheckHttp2HealthCheckOutputReference", jsii.get(self, "http2HealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="httpHealthCheck")
    def http_health_check(
        self,
    ) -> "GoogleComputeRegionHealthCheckHttpHealthCheckOutputReference":
        return typing.cast("GoogleComputeRegionHealthCheckHttpHealthCheckOutputReference", jsii.get(self, "httpHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="httpsHealthCheck")
    def https_health_check(
        self,
    ) -> "GoogleComputeRegionHealthCheckHttpsHealthCheckOutputReference":
        return typing.cast("GoogleComputeRegionHealthCheckHttpsHealthCheckOutputReference", jsii.get(self, "httpsHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="logConfig")
    def log_config(self) -> "GoogleComputeRegionHealthCheckLogConfigOutputReference":
        return typing.cast("GoogleComputeRegionHealthCheckLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="sslHealthCheck")
    def ssl_health_check(
        self,
    ) -> "GoogleComputeRegionHealthCheckSslHealthCheckOutputReference":
        return typing.cast("GoogleComputeRegionHealthCheckSslHealthCheckOutputReference", jsii.get(self, "sslHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="tcpHealthCheck")
    def tcp_health_check(
        self,
    ) -> "GoogleComputeRegionHealthCheckTcpHealthCheckOutputReference":
        return typing.cast("GoogleComputeRegionHealthCheckTcpHealthCheckOutputReference", jsii.get(self, "tcpHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleComputeRegionHealthCheckTimeoutsOutputReference":
        return typing.cast("GoogleComputeRegionHealthCheckTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="checkIntervalSecInput")
    def check_interval_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "checkIntervalSecInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcHealthCheckInput")
    def grpc_health_check_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionHealthCheckGrpcHealthCheck"]:
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckGrpcHealthCheck"], jsii.get(self, "grpcHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcTlsHealthCheckInput")
    def grpc_tls_health_check_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionHealthCheckGrpcTlsHealthCheck"]:
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckGrpcTlsHealthCheck"], jsii.get(self, "grpcTlsHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="healthyThresholdInput")
    def healthy_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthyThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="http2HealthCheckInput")
    def http2_health_check_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionHealthCheckHttp2HealthCheck"]:
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckHttp2HealthCheck"], jsii.get(self, "http2HealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHealthCheckInput")
    def http_health_check_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionHealthCheckHttpHealthCheck"]:
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckHttpHealthCheck"], jsii.get(self, "httpHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsHealthCheckInput")
    def https_health_check_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionHealthCheckHttpsHealthCheck"]:
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckHttpsHealthCheck"], jsii.get(self, "httpsHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigInput")
    def log_config_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionHealthCheckLogConfig"]:
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckLogConfig"], jsii.get(self, "logConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="sslHealthCheckInput")
    def ssl_health_check_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionHealthCheckSslHealthCheck"]:
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckSslHealthCheck"], jsii.get(self, "sslHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpHealthCheckInput")
    def tcp_health_check_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionHealthCheckTcpHealthCheck"]:
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckTcpHealthCheck"], jsii.get(self, "tcpHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecInput")
    def timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeRegionHealthCheckTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeRegionHealthCheckTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="unhealthyThresholdInput")
    def unhealthy_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unhealthyThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="checkIntervalSec")
    def check_interval_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "checkIntervalSec"))

    @check_interval_sec.setter
    def check_interval_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633a6d696240d1392ca45800ff4505968af3e5df81f2ebb2e841d22ae8d8177c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkIntervalSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71cbd6a1ea68092628cbb5170925fa6a360f6648748e1bb4f628b7bff38a67b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthyThreshold")
    def healthy_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthyThreshold"))

    @healthy_threshold.setter
    def healthy_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__992563d2e5772eead30b76d41b6d9c244e670afbdf240b04059ee46b0f439dd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthyThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c80850723679860413dd4c4185d7508d1ea83ba1533f4f2ddd370ceb7e1205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc26410f3ae76bff886ba2e690ec155726cbf2cd07850a3afa40afb794666e54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__057587284a800be6e679fadc550043f3cb82e6bf5a24834ac3e2c22e58734a17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1756fa9cef8cb8266b5b0ad3a345030149e2216eee030e270b8d8b0ffafb7438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSec")
    def timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSec"))

    @timeout_sec.setter
    def timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f120090f298a3c7573db92265e155bab49e75e22a4bfb5a86aa4ad3f6e7805d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unhealthyThreshold")
    def unhealthy_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unhealthyThreshold"))

    @unhealthy_threshold.setter
    def unhealthy_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9792baaf02e39fea03d980600a1a56a0d9d5bf41b247a348344c984c72e141c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unhealthyThreshold", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckConfig",
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
        "check_interval_sec": "checkIntervalSec",
        "description": "description",
        "grpc_health_check": "grpcHealthCheck",
        "grpc_tls_health_check": "grpcTlsHealthCheck",
        "healthy_threshold": "healthyThreshold",
        "http2_health_check": "http2HealthCheck",
        "http_health_check": "httpHealthCheck",
        "https_health_check": "httpsHealthCheck",
        "id": "id",
        "log_config": "logConfig",
        "project": "project",
        "region": "region",
        "ssl_health_check": "sslHealthCheck",
        "tcp_health_check": "tcpHealthCheck",
        "timeouts": "timeouts",
        "timeout_sec": "timeoutSec",
        "unhealthy_threshold": "unhealthyThreshold",
    },
)
class GoogleComputeRegionHealthCheckConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        check_interval_sec: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        grpc_health_check: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckGrpcHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_tls_health_check: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckGrpcTlsHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        healthy_threshold: typing.Optional[jsii.Number] = None,
        http2_health_check: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckHttp2HealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        http_health_check: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckHttpHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        https_health_check: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckHttpsHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        ssl_health_check: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckSslHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        tcp_health_check: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckTcpHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeRegionHealthCheckTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_sec: typing.Optional[jsii.Number] = None,
        unhealthy_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#name GoogleComputeRegionHealthCheck#name}
        :param check_interval_sec: How often (in seconds) to send a health check. The default value is 5 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#check_interval_sec GoogleComputeRegionHealthCheck#check_interval_sec}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#description GoogleComputeRegionHealthCheck#description}
        :param grpc_health_check: grpc_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#grpc_health_check GoogleComputeRegionHealthCheck#grpc_health_check}
        :param grpc_tls_health_check: grpc_tls_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#grpc_tls_health_check GoogleComputeRegionHealthCheck#grpc_tls_health_check}
        :param healthy_threshold: A so-far unhealthy instance will be marked healthy after this many consecutive successes. The default value is 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#healthy_threshold GoogleComputeRegionHealthCheck#healthy_threshold}
        :param http2_health_check: http2_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#http2_health_check GoogleComputeRegionHealthCheck#http2_health_check}
        :param http_health_check: http_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#http_health_check GoogleComputeRegionHealthCheck#http_health_check}
        :param https_health_check: https_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#https_health_check GoogleComputeRegionHealthCheck#https_health_check}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#id GoogleComputeRegionHealthCheck#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#log_config GoogleComputeRegionHealthCheck#log_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#project GoogleComputeRegionHealthCheck#project}.
        :param region: The Region in which the created health check should reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#region GoogleComputeRegionHealthCheck#region}
        :param ssl_health_check: ssl_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#ssl_health_check GoogleComputeRegionHealthCheck#ssl_health_check}
        :param tcp_health_check: tcp_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#tcp_health_check GoogleComputeRegionHealthCheck#tcp_health_check}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#timeouts GoogleComputeRegionHealthCheck#timeouts}
        :param timeout_sec: How long (in seconds) to wait before claiming failure. The default value is 5 seconds. It is invalid for timeoutSec to have greater value than checkIntervalSec. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#timeout_sec GoogleComputeRegionHealthCheck#timeout_sec}
        :param unhealthy_threshold: A so-far healthy instance will be marked unhealthy after this many consecutive failures. The default value is 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#unhealthy_threshold GoogleComputeRegionHealthCheck#unhealthy_threshold}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(grpc_health_check, dict):
            grpc_health_check = GoogleComputeRegionHealthCheckGrpcHealthCheck(**grpc_health_check)
        if isinstance(grpc_tls_health_check, dict):
            grpc_tls_health_check = GoogleComputeRegionHealthCheckGrpcTlsHealthCheck(**grpc_tls_health_check)
        if isinstance(http2_health_check, dict):
            http2_health_check = GoogleComputeRegionHealthCheckHttp2HealthCheck(**http2_health_check)
        if isinstance(http_health_check, dict):
            http_health_check = GoogleComputeRegionHealthCheckHttpHealthCheck(**http_health_check)
        if isinstance(https_health_check, dict):
            https_health_check = GoogleComputeRegionHealthCheckHttpsHealthCheck(**https_health_check)
        if isinstance(log_config, dict):
            log_config = GoogleComputeRegionHealthCheckLogConfig(**log_config)
        if isinstance(ssl_health_check, dict):
            ssl_health_check = GoogleComputeRegionHealthCheckSslHealthCheck(**ssl_health_check)
        if isinstance(tcp_health_check, dict):
            tcp_health_check = GoogleComputeRegionHealthCheckTcpHealthCheck(**tcp_health_check)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeRegionHealthCheckTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbea1cfc70fa55017169580102f017663d376074feda6f532aab0ff2e514c25d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument check_interval_sec", value=check_interval_sec, expected_type=type_hints["check_interval_sec"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument grpc_health_check", value=grpc_health_check, expected_type=type_hints["grpc_health_check"])
            check_type(argname="argument grpc_tls_health_check", value=grpc_tls_health_check, expected_type=type_hints["grpc_tls_health_check"])
            check_type(argname="argument healthy_threshold", value=healthy_threshold, expected_type=type_hints["healthy_threshold"])
            check_type(argname="argument http2_health_check", value=http2_health_check, expected_type=type_hints["http2_health_check"])
            check_type(argname="argument http_health_check", value=http_health_check, expected_type=type_hints["http_health_check"])
            check_type(argname="argument https_health_check", value=https_health_check, expected_type=type_hints["https_health_check"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_config", value=log_config, expected_type=type_hints["log_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument ssl_health_check", value=ssl_health_check, expected_type=type_hints["ssl_health_check"])
            check_type(argname="argument tcp_health_check", value=tcp_health_check, expected_type=type_hints["tcp_health_check"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument timeout_sec", value=timeout_sec, expected_type=type_hints["timeout_sec"])
            check_type(argname="argument unhealthy_threshold", value=unhealthy_threshold, expected_type=type_hints["unhealthy_threshold"])
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
        if check_interval_sec is not None:
            self._values["check_interval_sec"] = check_interval_sec
        if description is not None:
            self._values["description"] = description
        if grpc_health_check is not None:
            self._values["grpc_health_check"] = grpc_health_check
        if grpc_tls_health_check is not None:
            self._values["grpc_tls_health_check"] = grpc_tls_health_check
        if healthy_threshold is not None:
            self._values["healthy_threshold"] = healthy_threshold
        if http2_health_check is not None:
            self._values["http2_health_check"] = http2_health_check
        if http_health_check is not None:
            self._values["http_health_check"] = http_health_check
        if https_health_check is not None:
            self._values["https_health_check"] = https_health_check
        if id is not None:
            self._values["id"] = id
        if log_config is not None:
            self._values["log_config"] = log_config
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if ssl_health_check is not None:
            self._values["ssl_health_check"] = ssl_health_check
        if tcp_health_check is not None:
            self._values["tcp_health_check"] = tcp_health_check
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if timeout_sec is not None:
            self._values["timeout_sec"] = timeout_sec
        if unhealthy_threshold is not None:
            self._values["unhealthy_threshold"] = unhealthy_threshold

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
        RFC1035.  Specifically, the name must be 1-63 characters long and
        match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means
        the first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the
        last character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#name GoogleComputeRegionHealthCheck#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def check_interval_sec(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to send a health check. The default value is 5 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#check_interval_sec GoogleComputeRegionHealthCheck#check_interval_sec}
        '''
        result = self._values.get("check_interval_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#description GoogleComputeRegionHealthCheck#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grpc_health_check(
        self,
    ) -> typing.Optional["GoogleComputeRegionHealthCheckGrpcHealthCheck"]:
        '''grpc_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#grpc_health_check GoogleComputeRegionHealthCheck#grpc_health_check}
        '''
        result = self._values.get("grpc_health_check")
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckGrpcHealthCheck"], result)

    @builtins.property
    def grpc_tls_health_check(
        self,
    ) -> typing.Optional["GoogleComputeRegionHealthCheckGrpcTlsHealthCheck"]:
        '''grpc_tls_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#grpc_tls_health_check GoogleComputeRegionHealthCheck#grpc_tls_health_check}
        '''
        result = self._values.get("grpc_tls_health_check")
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckGrpcTlsHealthCheck"], result)

    @builtins.property
    def healthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''A so-far unhealthy instance will be marked healthy after this many consecutive successes. The default value is 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#healthy_threshold GoogleComputeRegionHealthCheck#healthy_threshold}
        '''
        result = self._values.get("healthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def http2_health_check(
        self,
    ) -> typing.Optional["GoogleComputeRegionHealthCheckHttp2HealthCheck"]:
        '''http2_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#http2_health_check GoogleComputeRegionHealthCheck#http2_health_check}
        '''
        result = self._values.get("http2_health_check")
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckHttp2HealthCheck"], result)

    @builtins.property
    def http_health_check(
        self,
    ) -> typing.Optional["GoogleComputeRegionHealthCheckHttpHealthCheck"]:
        '''http_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#http_health_check GoogleComputeRegionHealthCheck#http_health_check}
        '''
        result = self._values.get("http_health_check")
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckHttpHealthCheck"], result)

    @builtins.property
    def https_health_check(
        self,
    ) -> typing.Optional["GoogleComputeRegionHealthCheckHttpsHealthCheck"]:
        '''https_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#https_health_check GoogleComputeRegionHealthCheck#https_health_check}
        '''
        result = self._values.get("https_health_check")
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckHttpsHealthCheck"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#id GoogleComputeRegionHealthCheck#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_config(self) -> typing.Optional["GoogleComputeRegionHealthCheckLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#log_config GoogleComputeRegionHealthCheck#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckLogConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#project GoogleComputeRegionHealthCheck#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The Region in which the created health check should reside. If it is not provided, the provider region is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#region GoogleComputeRegionHealthCheck#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_health_check(
        self,
    ) -> typing.Optional["GoogleComputeRegionHealthCheckSslHealthCheck"]:
        '''ssl_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#ssl_health_check GoogleComputeRegionHealthCheck#ssl_health_check}
        '''
        result = self._values.get("ssl_health_check")
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckSslHealthCheck"], result)

    @builtins.property
    def tcp_health_check(
        self,
    ) -> typing.Optional["GoogleComputeRegionHealthCheckTcpHealthCheck"]:
        '''tcp_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#tcp_health_check GoogleComputeRegionHealthCheck#tcp_health_check}
        '''
        result = self._values.get("tcp_health_check")
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckTcpHealthCheck"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeRegionHealthCheckTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#timeouts GoogleComputeRegionHealthCheck#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeRegionHealthCheckTimeouts"], result)

    @builtins.property
    def timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''How long (in seconds) to wait before claiming failure.

        The default value is 5 seconds.  It is invalid for timeoutSec to have
        greater value than checkIntervalSec.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#timeout_sec GoogleComputeRegionHealthCheck#timeout_sec}
        '''
        result = self._values.get("timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''A so-far healthy instance will be marked unhealthy after this many consecutive failures. The default value is 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#unhealthy_threshold GoogleComputeRegionHealthCheck#unhealthy_threshold}
        '''
        result = self._values.get("unhealthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionHealthCheckConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckGrpcHealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "grpc_service_name": "grpcServiceName",
        "port": "port",
        "port_name": "portName",
        "port_specification": "portSpecification",
    },
)
class GoogleComputeRegionHealthCheckGrpcHealthCheck:
    def __init__(
        self,
        *,
        grpc_service_name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        port_name: typing.Optional[builtins.str] = None,
        port_specification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param grpc_service_name: The gRPC service name for the health check. The value of grpcServiceName has the following meanings by convention:. - Empty serviceName means the overall status of all services at the backend. - Non-empty serviceName means the health of that gRPC service, as defined by the owner of the service. The grpcServiceName can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#grpc_service_name GoogleComputeRegionHealthCheck#grpc_service_name}
        :param port: The port number for the health check request. Must be specified if portName and portSpecification are not set or if port_specification is USE_FIXED_PORT. Valid values are 1 through 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, gRPC health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc3edbd700a76959587bce69411dd7995a3683c595b4fe36c5e1e66f05b07193)
            check_type(argname="argument grpc_service_name", value=grpc_service_name, expected_type=type_hints["grpc_service_name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument port_name", value=port_name, expected_type=type_hints["port_name"])
            check_type(argname="argument port_specification", value=port_specification, expected_type=type_hints["port_specification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if grpc_service_name is not None:
            self._values["grpc_service_name"] = grpc_service_name
        if port is not None:
            self._values["port"] = port
        if port_name is not None:
            self._values["port_name"] = port_name
        if port_specification is not None:
            self._values["port_specification"] = port_specification

    @builtins.property
    def grpc_service_name(self) -> typing.Optional[builtins.str]:
        '''The gRPC service name for the health check. The value of grpcServiceName has the following meanings by convention:.

        - Empty serviceName means the overall status of all services at the backend.
        - Non-empty serviceName means the health of that gRPC service, as defined by the owner of the service.

        The grpcServiceName can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#grpc_service_name GoogleComputeRegionHealthCheck#grpc_service_name}
        '''
        result = self._values.get("grpc_service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port number for the health check request.

        Must be specified if portName and portSpecification are not set
        or if port_specification is USE_FIXED_PORT. Valid values are 1 through 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        '''
        result = self._values.get("port_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_specification(self) -> typing.Optional[builtins.str]:
        '''Specifies how port is selected for health checking, can be one of the following values:.

        - 'USE_FIXED_PORT': The port number in 'port' is used for health checking.

          - 'USE_NAMED_PORT': The 'portName' is used for health checking.
          - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each
            network endpoint is used for health checking. For other backends, the
            port or named port specified in the Backend Service is used for health
            checking.

        If not specified, gRPC health check follows behavior specified in 'port' and
        'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionHealthCheckGrpcHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionHealthCheckGrpcHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckGrpcHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92a1f2c57786f918bc8783fb00c98a64b39c023171cada940083d5cda98d2cba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGrpcServiceName")
    def reset_grpc_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpcServiceName", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPortName")
    def reset_port_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortName", []))

    @jsii.member(jsii_name="resetPortSpecification")
    def reset_port_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortSpecification", []))

    @builtins.property
    @jsii.member(jsii_name="grpcServiceNameInput")
    def grpc_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grpcServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="portNameInput")
    def port_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portNameInput"))

    @builtins.property
    @jsii.member(jsii_name="portSpecificationInput")
    def port_specification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portSpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcServiceName")
    def grpc_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grpcServiceName"))

    @grpc_service_name.setter
    def grpc_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0facb01a9262a1c87a7f8def380689a0b80375c32437665696220fbcd0996f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grpcServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ece6fa826407e7309bc95c2638b7e98299c13ce09be7009f0b9920bbb688228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab266b6be5d8634b4f85d753facb4021222b3638a38fefb29862a1b31b2cf57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a19332f85ac499c5bb61595b09ee8397c4a8e418e54e6cb9dbafd9497986575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionHealthCheckGrpcHealthCheck]:
        return typing.cast(typing.Optional[GoogleComputeRegionHealthCheckGrpcHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionHealthCheckGrpcHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9d8bc276959a5884396b21cf4b18816b833166693c7924ed6482b9197776bae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckGrpcTlsHealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "grpc_service_name": "grpcServiceName",
        "port": "port",
        "port_specification": "portSpecification",
    },
)
class GoogleComputeRegionHealthCheckGrpcTlsHealthCheck:
    def __init__(
        self,
        *,
        grpc_service_name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        port_specification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param grpc_service_name: The gRPC service name for the health check. The value of grpcServiceName has the following meanings by convention:. - Empty serviceName means the overall status of all services at the backend. - Non-empty serviceName means the health of that gRPC service, as defined by the owner of the service. The grpcServiceName can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#grpc_service_name GoogleComputeRegionHealthCheck#grpc_service_name}
        :param port: The port number for the health check request. Must be specified if port_specification is USE_FIXED_PORT. Valid values are 1 through 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': Not supported for GRPC with TLS health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, gRPC health check follows behavior specified in the 'port' field. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ee93a470e7cc52d2bbfbd6ce0bdbaf730f1e77ff7fb25dcb3655acdb90afd20)
            check_type(argname="argument grpc_service_name", value=grpc_service_name, expected_type=type_hints["grpc_service_name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument port_specification", value=port_specification, expected_type=type_hints["port_specification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if grpc_service_name is not None:
            self._values["grpc_service_name"] = grpc_service_name
        if port is not None:
            self._values["port"] = port
        if port_specification is not None:
            self._values["port_specification"] = port_specification

    @builtins.property
    def grpc_service_name(self) -> typing.Optional[builtins.str]:
        '''The gRPC service name for the health check. The value of grpcServiceName has the following meanings by convention:.

        - Empty serviceName means the overall status of all services at the backend.
        - Non-empty serviceName means the health of that gRPC service, as defined by the owner of the service.

        The grpcServiceName can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#grpc_service_name GoogleComputeRegionHealthCheck#grpc_service_name}
        '''
        result = self._values.get("grpc_service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port number for the health check request.

        Must be specified if port_specification is USE_FIXED_PORT. Valid values are 1 through 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_specification(self) -> typing.Optional[builtins.str]:
        '''Specifies how port is selected for health checking, can be one of the following values:.

        - 'USE_FIXED_PORT': The port number in 'port' is used for health checking.

          - 'USE_NAMED_PORT': Not supported for GRPC with TLS health checking.
          - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each
            network endpoint is used for health checking. For other backends, the
            port or named port specified in the Backend Service is used for health
            checking.

        If not specified, gRPC health check follows behavior specified in the 'port' field. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionHealthCheckGrpcTlsHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionHealthCheckGrpcTlsHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckGrpcTlsHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e6bbb065315d943996fa1fb06244b6da0a9d70c0e2d442563107722e7b606c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGrpcServiceName")
    def reset_grpc_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpcServiceName", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPortSpecification")
    def reset_port_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortSpecification", []))

    @builtins.property
    @jsii.member(jsii_name="grpcServiceNameInput")
    def grpc_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grpcServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="portSpecificationInput")
    def port_specification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portSpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcServiceName")
    def grpc_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grpcServiceName"))

    @grpc_service_name.setter
    def grpc_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7167b97c78387ced69d04df31809e423e9065e3f1eec6344e7373f3fecdd074e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grpcServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7eb7155e5401a741713100f224d0b767a0a8f72b3430efc3322c38831200ab4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f5dc4a64ca0d0ef4d84884923839dd7d950dbccb78291611bde1dc277d6b08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionHealthCheckGrpcTlsHealthCheck]:
        return typing.cast(typing.Optional[GoogleComputeRegionHealthCheckGrpcTlsHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionHealthCheckGrpcTlsHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff77872a3c1e7061fbe80391cddaff1c03e6a7b79e51b3084ea8548faf022107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckHttp2HealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "port": "port",
        "port_name": "portName",
        "port_specification": "portSpecification",
        "proxy_header": "proxyHeader",
        "request_path": "requestPath",
        "response": "response",
    },
)
class GoogleComputeRegionHealthCheckHttp2HealthCheck:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        port_name: typing.Optional[builtins.str] = None,
        port_specification: typing.Optional[builtins.str] = None,
        proxy_header: typing.Optional[builtins.str] = None,
        request_path: typing.Optional[builtins.str] = None,
        response: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: The value of the host header in the HTTP2 health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#host GoogleComputeRegionHealthCheck#host}
        :param port: The TCP port number for the HTTP2 health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTP2 health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#proxy_header GoogleComputeRegionHealthCheck#proxy_header}
        :param request_path: The request path of the HTTP2 health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#request_path GoogleComputeRegionHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#response GoogleComputeRegionHealthCheck#response}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69c1a7a30de92f4d76051549cd05e8291773164f7c7bf9c6883774643e95aec)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument port_name", value=port_name, expected_type=type_hints["port_name"])
            check_type(argname="argument port_specification", value=port_specification, expected_type=type_hints["port_specification"])
            check_type(argname="argument proxy_header", value=proxy_header, expected_type=type_hints["proxy_header"])
            check_type(argname="argument request_path", value=request_path, expected_type=type_hints["request_path"])
            check_type(argname="argument response", value=response, expected_type=type_hints["response"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host is not None:
            self._values["host"] = host
        if port is not None:
            self._values["port"] = port
        if port_name is not None:
            self._values["port_name"] = port_name
        if port_specification is not None:
            self._values["port_specification"] = port_specification
        if proxy_header is not None:
            self._values["proxy_header"] = proxy_header
        if request_path is not None:
            self._values["request_path"] = request_path
        if response is not None:
            self._values["response"] = response

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The value of the host header in the HTTP2 health check request.

        If left empty (default value), the public IP on behalf of which this health
        check is performed will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#host GoogleComputeRegionHealthCheck#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The TCP port number for the HTTP2 health check request. The default value is 443.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        '''
        result = self._values.get("port_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_specification(self) -> typing.Optional[builtins.str]:
        '''Specifies how port is selected for health checking, can be one of the following values:.

        - 'USE_FIXED_PORT': The port number in 'port' is used for health checking.

          - 'USE_NAMED_PORT': The 'portName' is used for health checking.
          - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each
            network endpoint is used for health checking. For other backends, the
            port or named port specified in the Backend Service is used for health
            checking.

        If not specified, HTTP2 health check follows behavior specified in 'port' and
        'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_header(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of proxy header to append before sending data to the backend.

        Default value: "NONE" Possible values: ["NONE", "PROXY_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#proxy_header GoogleComputeRegionHealthCheck#proxy_header}
        '''
        result = self._values.get("proxy_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_path(self) -> typing.Optional[builtins.str]:
        '''The request path of the HTTP2 health check request. The default value is /.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#request_path GoogleComputeRegionHealthCheck#request_path}
        '''
        result = self._values.get("request_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''The bytes to match against the beginning of the response data.

        If left empty
        (the default value), any response will indicate health. The response data
        can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#response GoogleComputeRegionHealthCheck#response}
        '''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionHealthCheckHttp2HealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionHealthCheckHttp2HealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckHttp2HealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__589a4914b26bd51936f0a003748f6d940f081d949febd66b62b23679b3074532)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPortName")
    def reset_port_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortName", []))

    @jsii.member(jsii_name="resetPortSpecification")
    def reset_port_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortSpecification", []))

    @jsii.member(jsii_name="resetProxyHeader")
    def reset_proxy_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyHeader", []))

    @jsii.member(jsii_name="resetRequestPath")
    def reset_request_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestPath", []))

    @jsii.member(jsii_name="resetResponse")
    def reset_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponse", []))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="portNameInput")
    def port_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portNameInput"))

    @builtins.property
    @jsii.member(jsii_name="portSpecificationInput")
    def port_specification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portSpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyHeaderInput")
    def proxy_header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="requestPathInput")
    def request_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestPathInput"))

    @builtins.property
    @jsii.member(jsii_name="responseInput")
    def response_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ddf1c0170bb487e7d9d7010851e16f1eb32b71233099a190674fc22a4985f51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1af4edddfec0da1a038e760ad52ed772f2abe95f4e6739f1c7a08607dd61e41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b17af42a6113585668b7e09d822075f49d0f7b5b427b29b604f22cf95b76c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78af8a811e31cf3fedfe0dcabe9221549078941af3062146158aaa2b7a641eb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyHeader")
    def proxy_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyHeader"))

    @proxy_header.setter
    def proxy_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__907981b9596219f8b73a1c6028d3a90e01ede4109788663a08ffce4e61f05a50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestPath")
    def request_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestPath"))

    @request_path.setter
    def request_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf0969bb83e83d64a10761a65fd50640ce4d8c5293a6241da0dc59fb1c1da474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4048304e7ac3576608083e51df7f28da0fdf70c3b5e3b0a9aa3454d8b6cb801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionHealthCheckHttp2HealthCheck]:
        return typing.cast(typing.Optional[GoogleComputeRegionHealthCheckHttp2HealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionHealthCheckHttp2HealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c82e100a2f3d3d48b5911d49b16837726d3f83d962e8d4ba8f132653727e4ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckHttpHealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "port": "port",
        "port_name": "portName",
        "port_specification": "portSpecification",
        "proxy_header": "proxyHeader",
        "request_path": "requestPath",
        "response": "response",
    },
)
class GoogleComputeRegionHealthCheckHttpHealthCheck:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        port_name: typing.Optional[builtins.str] = None,
        port_specification: typing.Optional[builtins.str] = None,
        proxy_header: typing.Optional[builtins.str] = None,
        request_path: typing.Optional[builtins.str] = None,
        response: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: The value of the host header in the HTTP health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#host GoogleComputeRegionHealthCheck#host}
        :param port: The TCP port number for the HTTP health check request. The default value is 80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTP health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#proxy_header GoogleComputeRegionHealthCheck#proxy_header}
        :param request_path: The request path of the HTTP health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#request_path GoogleComputeRegionHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#response GoogleComputeRegionHealthCheck#response}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81fba5e77cb9831e91926eee942526364f18135ad0d826013f809fdd37371848)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument port_name", value=port_name, expected_type=type_hints["port_name"])
            check_type(argname="argument port_specification", value=port_specification, expected_type=type_hints["port_specification"])
            check_type(argname="argument proxy_header", value=proxy_header, expected_type=type_hints["proxy_header"])
            check_type(argname="argument request_path", value=request_path, expected_type=type_hints["request_path"])
            check_type(argname="argument response", value=response, expected_type=type_hints["response"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host is not None:
            self._values["host"] = host
        if port is not None:
            self._values["port"] = port
        if port_name is not None:
            self._values["port_name"] = port_name
        if port_specification is not None:
            self._values["port_specification"] = port_specification
        if proxy_header is not None:
            self._values["proxy_header"] = proxy_header
        if request_path is not None:
            self._values["request_path"] = request_path
        if response is not None:
            self._values["response"] = response

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The value of the host header in the HTTP health check request.

        If left empty (default value), the public IP on behalf of which this health
        check is performed will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#host GoogleComputeRegionHealthCheck#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The TCP port number for the HTTP health check request. The default value is 80.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        '''
        result = self._values.get("port_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_specification(self) -> typing.Optional[builtins.str]:
        '''Specifies how port is selected for health checking, can be one of the following values:.

        - 'USE_FIXED_PORT': The port number in 'port' is used for health checking.

          - 'USE_NAMED_PORT': The 'portName' is used for health checking.
          - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each
            network endpoint is used for health checking. For other backends, the
            port or named port specified in the Backend Service is used for health
            checking.

        If not specified, HTTP health check follows behavior specified in 'port' and
        'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_header(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of proxy header to append before sending data to the backend.

        Default value: "NONE" Possible values: ["NONE", "PROXY_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#proxy_header GoogleComputeRegionHealthCheck#proxy_header}
        '''
        result = self._values.get("proxy_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_path(self) -> typing.Optional[builtins.str]:
        '''The request path of the HTTP health check request. The default value is /.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#request_path GoogleComputeRegionHealthCheck#request_path}
        '''
        result = self._values.get("request_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''The bytes to match against the beginning of the response data.

        If left empty
        (the default value), any response will indicate health. The response data
        can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#response GoogleComputeRegionHealthCheck#response}
        '''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionHealthCheckHttpHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionHealthCheckHttpHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckHttpHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af5912fb352990ef0e6dc9e3ac195962392cc2956e9b0558878df069d899ee7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPortName")
    def reset_port_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortName", []))

    @jsii.member(jsii_name="resetPortSpecification")
    def reset_port_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortSpecification", []))

    @jsii.member(jsii_name="resetProxyHeader")
    def reset_proxy_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyHeader", []))

    @jsii.member(jsii_name="resetRequestPath")
    def reset_request_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestPath", []))

    @jsii.member(jsii_name="resetResponse")
    def reset_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponse", []))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="portNameInput")
    def port_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portNameInput"))

    @builtins.property
    @jsii.member(jsii_name="portSpecificationInput")
    def port_specification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portSpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyHeaderInput")
    def proxy_header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="requestPathInput")
    def request_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestPathInput"))

    @builtins.property
    @jsii.member(jsii_name="responseInput")
    def response_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62989391614d3c778fc99ea621034ee6c82bc714b422a9aaac2665fe6e831c8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fad2d14b52e72c82cda54721bc2e12b222f60244fc6993b7784231ca01c062f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19bf954a5fb2843f5544fa61805c0f79c52fc3cf03f6f55d49959341a6460b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844bd009bb620a03887789056ab7e70a4d0a3ed9bce4e9781dbc6716522a422f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyHeader")
    def proxy_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyHeader"))

    @proxy_header.setter
    def proxy_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a824ded576cfda3feda43249c3a7b1b460c8fa6d8f9aa02f083262caac92901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestPath")
    def request_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestPath"))

    @request_path.setter
    def request_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__534f2a6be61fc1b08793f440502e368ac5744cc0aba4617f95f64d107ded80aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9eae331a80db55dddd9169f273ea193f906661c3c51c462303ca7aa40fc10d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionHealthCheckHttpHealthCheck]:
        return typing.cast(typing.Optional[GoogleComputeRegionHealthCheckHttpHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionHealthCheckHttpHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f94b0c47b75e5adb69c9afee400dd5ea9460db72d375d51ff686e1de5790dd39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckHttpsHealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "port": "port",
        "port_name": "portName",
        "port_specification": "portSpecification",
        "proxy_header": "proxyHeader",
        "request_path": "requestPath",
        "response": "response",
    },
)
class GoogleComputeRegionHealthCheckHttpsHealthCheck:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        port_name: typing.Optional[builtins.str] = None,
        port_specification: typing.Optional[builtins.str] = None,
        proxy_header: typing.Optional[builtins.str] = None,
        request_path: typing.Optional[builtins.str] = None,
        response: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: The value of the host header in the HTTPS health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#host GoogleComputeRegionHealthCheck#host}
        :param port: The TCP port number for the HTTPS health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTPS health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#proxy_header GoogleComputeRegionHealthCheck#proxy_header}
        :param request_path: The request path of the HTTPS health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#request_path GoogleComputeRegionHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#response GoogleComputeRegionHealthCheck#response}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__224bcc7e58670676a4abb26812c3477d991a91897988867c03d0f00f99442cd4)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument port_name", value=port_name, expected_type=type_hints["port_name"])
            check_type(argname="argument port_specification", value=port_specification, expected_type=type_hints["port_specification"])
            check_type(argname="argument proxy_header", value=proxy_header, expected_type=type_hints["proxy_header"])
            check_type(argname="argument request_path", value=request_path, expected_type=type_hints["request_path"])
            check_type(argname="argument response", value=response, expected_type=type_hints["response"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host is not None:
            self._values["host"] = host
        if port is not None:
            self._values["port"] = port
        if port_name is not None:
            self._values["port_name"] = port_name
        if port_specification is not None:
            self._values["port_specification"] = port_specification
        if proxy_header is not None:
            self._values["proxy_header"] = proxy_header
        if request_path is not None:
            self._values["request_path"] = request_path
        if response is not None:
            self._values["response"] = response

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The value of the host header in the HTTPS health check request.

        If left empty (default value), the public IP on behalf of which this health
        check is performed will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#host GoogleComputeRegionHealthCheck#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The TCP port number for the HTTPS health check request. The default value is 443.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        '''
        result = self._values.get("port_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_specification(self) -> typing.Optional[builtins.str]:
        '''Specifies how port is selected for health checking, can be one of the following values:.

        - 'USE_FIXED_PORT': The port number in 'port' is used for health checking.

          - 'USE_NAMED_PORT': The 'portName' is used for health checking.
          - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each
            network endpoint is used for health checking. For other backends, the
            port or named port specified in the Backend Service is used for health
            checking.

        If not specified, HTTPS health check follows behavior specified in 'port' and
        'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_header(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of proxy header to append before sending data to the backend.

        Default value: "NONE" Possible values: ["NONE", "PROXY_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#proxy_header GoogleComputeRegionHealthCheck#proxy_header}
        '''
        result = self._values.get("proxy_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_path(self) -> typing.Optional[builtins.str]:
        '''The request path of the HTTPS health check request. The default value is /.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#request_path GoogleComputeRegionHealthCheck#request_path}
        '''
        result = self._values.get("request_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''The bytes to match against the beginning of the response data.

        If left empty
        (the default value), any response will indicate health. The response data
        can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#response GoogleComputeRegionHealthCheck#response}
        '''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionHealthCheckHttpsHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionHealthCheckHttpsHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckHttpsHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3648df0f32789244d2a6268d8568aae9c6b0ca72f44854b9c465b390e6e39dcd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPortName")
    def reset_port_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortName", []))

    @jsii.member(jsii_name="resetPortSpecification")
    def reset_port_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortSpecification", []))

    @jsii.member(jsii_name="resetProxyHeader")
    def reset_proxy_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyHeader", []))

    @jsii.member(jsii_name="resetRequestPath")
    def reset_request_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestPath", []))

    @jsii.member(jsii_name="resetResponse")
    def reset_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponse", []))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="portNameInput")
    def port_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portNameInput"))

    @builtins.property
    @jsii.member(jsii_name="portSpecificationInput")
    def port_specification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portSpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyHeaderInput")
    def proxy_header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="requestPathInput")
    def request_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestPathInput"))

    @builtins.property
    @jsii.member(jsii_name="responseInput")
    def response_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f28d47099aed11df8fffb242a15a44abf79574c453d0cb7e9a66087dec6faee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0778e188d7848764e23fd600752aa7b76d8fe3eef3969fed023b1b8995bf66a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda69792a9022b0db5202e0fa0b08ec2c54ad0c5c66926770b6e758e8794cad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece668167637bd0ea53b50e3bf14d5538dff623072c64f98f5e42c232f4cbe02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyHeader")
    def proxy_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyHeader"))

    @proxy_header.setter
    def proxy_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da15a126b8dfcef4eac107fd23dab4dd23c88b1fa6092850ff838ee508eec5c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestPath")
    def request_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestPath"))

    @request_path.setter
    def request_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64c607ebd62fe7cee7775d5a84f7f5a91d796427b83775fb7b987897992c5e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__846efc491a2040a786b51bfe50d568f65e8c682c6033db5a4a6bcf15e434101d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionHealthCheckHttpsHealthCheck]:
        return typing.cast(typing.Optional[GoogleComputeRegionHealthCheckHttpsHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionHealthCheckHttpsHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be2d2d1bc1f189eb4643bdf49b6d9fe3d92b036e1b0932bd00d40e26b8d12a4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckLogConfig",
    jsii_struct_bases=[],
    name_mapping={"enable": "enable"},
)
class GoogleComputeRegionHealthCheckLogConfig:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable: Indicates whether or not to export logs. This is false by default, which means no health check logging will be done. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#enable GoogleComputeRegionHealthCheck#enable}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c850f00d1d35fa87a60c6392e6087a8ce9bdc8691399db0e351cdc0a1b64342)
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable is not None:
            self._values["enable"] = enable

    @builtins.property
    def enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether or not to export logs.

        This is false by default,
        which means no health check logging will be done.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#enable GoogleComputeRegionHealthCheck#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionHealthCheckLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionHealthCheckLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bbe9beeea1caffcd43313b10253fe074e958e91ddee499731c915cf42f3c24e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnable")
    def reset_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnable", []))

    @builtins.property
    @jsii.member(jsii_name="enableInput")
    def enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__35048e9a9b88cb4881b1f30fe7eb96830b933bb85f830e4bcb2a4735aefefbf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionHealthCheckLogConfig]:
        return typing.cast(typing.Optional[GoogleComputeRegionHealthCheckLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionHealthCheckLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3d9b54c2a44c9a12bbe0638c34cdf50b0714cab7e8353f4b9843dd429a5df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckSslHealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "port_name": "portName",
        "port_specification": "portSpecification",
        "proxy_header": "proxyHeader",
        "request": "request",
        "response": "response",
    },
)
class GoogleComputeRegionHealthCheckSslHealthCheck:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        port_name: typing.Optional[builtins.str] = None,
        port_specification: typing.Optional[builtins.str] = None,
        proxy_header: typing.Optional[builtins.str] = None,
        request: typing.Optional[builtins.str] = None,
        response: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: The TCP port number for the SSL health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, SSL health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#proxy_header GoogleComputeRegionHealthCheck#proxy_header}
        :param request: The application data to send once the SSL connection has been established (default value is empty). If both request and response are empty, the connection establishment alone will indicate health. The request data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#request GoogleComputeRegionHealthCheck#request}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#response GoogleComputeRegionHealthCheck#response}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9111b4cae3cdda47160d40c3ba5b33da79f94a91dc692250f598e7f2638336a6)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument port_name", value=port_name, expected_type=type_hints["port_name"])
            check_type(argname="argument port_specification", value=port_specification, expected_type=type_hints["port_specification"])
            check_type(argname="argument proxy_header", value=proxy_header, expected_type=type_hints["proxy_header"])
            check_type(argname="argument request", value=request, expected_type=type_hints["request"])
            check_type(argname="argument response", value=response, expected_type=type_hints["response"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port
        if port_name is not None:
            self._values["port_name"] = port_name
        if port_specification is not None:
            self._values["port_specification"] = port_specification
        if proxy_header is not None:
            self._values["proxy_header"] = proxy_header
        if request is not None:
            self._values["request"] = request
        if response is not None:
            self._values["response"] = response

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The TCP port number for the SSL health check request. The default value is 443.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        '''
        result = self._values.get("port_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_specification(self) -> typing.Optional[builtins.str]:
        '''Specifies how port is selected for health checking, can be one of the following values:.

        - 'USE_FIXED_PORT': The port number in 'port' is used for health checking.

          - 'USE_NAMED_PORT': The 'portName' is used for health checking.
          - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each
            network endpoint is used for health checking. For other backends, the
            port or named port specified in the Backend Service is used for health
            checking.

        If not specified, SSL health check follows behavior specified in 'port' and
        'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_header(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of proxy header to append before sending data to the backend.

        Default value: "NONE" Possible values: ["NONE", "PROXY_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#proxy_header GoogleComputeRegionHealthCheck#proxy_header}
        '''
        result = self._values.get("proxy_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request(self) -> typing.Optional[builtins.str]:
        '''The application data to send once the SSL connection has been established (default value is empty).

        If both request and response are
        empty, the connection establishment alone will indicate health. The request
        data can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#request GoogleComputeRegionHealthCheck#request}
        '''
        result = self._values.get("request")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''The bytes to match against the beginning of the response data.

        If left empty
        (the default value), any response will indicate health. The response data
        can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#response GoogleComputeRegionHealthCheck#response}
        '''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionHealthCheckSslHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionHealthCheckSslHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckSslHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0170f44f2b3a341549f5aab8174f4dc4050857c6533c03e2c57d3472500530c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPortName")
    def reset_port_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortName", []))

    @jsii.member(jsii_name="resetPortSpecification")
    def reset_port_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortSpecification", []))

    @jsii.member(jsii_name="resetProxyHeader")
    def reset_proxy_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyHeader", []))

    @jsii.member(jsii_name="resetRequest")
    def reset_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequest", []))

    @jsii.member(jsii_name="resetResponse")
    def reset_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponse", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="portNameInput")
    def port_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portNameInput"))

    @builtins.property
    @jsii.member(jsii_name="portSpecificationInput")
    def port_specification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portSpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyHeaderInput")
    def proxy_header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="requestInput")
    def request_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestInput"))

    @builtins.property
    @jsii.member(jsii_name="responseInput")
    def response_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43841606de3ca3999d442124ba96e1243569c54d4b0481c9014267188bb77f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef30335c9b7f1df9ab144765b99856c41dd0e22947fb6c76d8cb85b6b7aed071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ab92ded1b56ef3fe9134d0825cc5e26582365f5dcde68638c85c4715a5bb70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyHeader")
    def proxy_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyHeader"))

    @proxy_header.setter
    def proxy_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2751e1c13276969e4b5e7e17741e5338ea5510259062012a8f440305bb0f709d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="request")
    def request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "request"))

    @request.setter
    def request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53457507b5e8c2b8c29d8300b1c1552a49ccf7a072cae9b8c71aab74182ebf7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "request", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fad0a60846b969c65184b5cf0e0a2404556aa6f3438ca2514ab423c5149e153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionHealthCheckSslHealthCheck]:
        return typing.cast(typing.Optional[GoogleComputeRegionHealthCheckSslHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionHealthCheckSslHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d86f9f22ec2bf170e076bb6707e2d87b8d477c9103fc3ac401bfaf035efad736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckTcpHealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "port_name": "portName",
        "port_specification": "portSpecification",
        "proxy_header": "proxyHeader",
        "request": "request",
        "response": "response",
    },
)
class GoogleComputeRegionHealthCheckTcpHealthCheck:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        port_name: typing.Optional[builtins.str] = None,
        port_specification: typing.Optional[builtins.str] = None,
        proxy_header: typing.Optional[builtins.str] = None,
        request: typing.Optional[builtins.str] = None,
        response: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: The TCP port number for the TCP health check request. The default value is 80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, TCP health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#proxy_header GoogleComputeRegionHealthCheck#proxy_header}
        :param request: The application data to send once the TCP connection has been established (default value is empty). If both request and response are empty, the connection establishment alone will indicate health. The request data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#request GoogleComputeRegionHealthCheck#request}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#response GoogleComputeRegionHealthCheck#response}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430c9756617ec319eafbb587da46878fb1626a76638d2af2f332ed12118494cf)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument port_name", value=port_name, expected_type=type_hints["port_name"])
            check_type(argname="argument port_specification", value=port_specification, expected_type=type_hints["port_specification"])
            check_type(argname="argument proxy_header", value=proxy_header, expected_type=type_hints["proxy_header"])
            check_type(argname="argument request", value=request, expected_type=type_hints["request"])
            check_type(argname="argument response", value=response, expected_type=type_hints["response"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port
        if port_name is not None:
            self._values["port_name"] = port_name
        if port_specification is not None:
            self._values["port_specification"] = port_specification
        if proxy_header is not None:
            self._values["proxy_header"] = proxy_header
        if request is not None:
            self._values["request"] = request
        if response is not None:
            self._values["response"] = response

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The TCP port number for the TCP health check request. The default value is 80.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port GoogleComputeRegionHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_name GoogleComputeRegionHealthCheck#port_name}
        '''
        result = self._values.get("port_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_specification(self) -> typing.Optional[builtins.str]:
        '''Specifies how port is selected for health checking, can be one of the following values:.

        - 'USE_FIXED_PORT': The port number in 'port' is used for health checking.

          - 'USE_NAMED_PORT': The 'portName' is used for health checking.
          - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each
            network endpoint is used for health checking. For other backends, the
            port or named port specified in the Backend Service is used for health
            checking.

        If not specified, TCP health check follows behavior specified in 'port' and
        'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#port_specification GoogleComputeRegionHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_header(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of proxy header to append before sending data to the backend.

        Default value: "NONE" Possible values: ["NONE", "PROXY_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#proxy_header GoogleComputeRegionHealthCheck#proxy_header}
        '''
        result = self._values.get("proxy_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request(self) -> typing.Optional[builtins.str]:
        '''The application data to send once the TCP connection has been established (default value is empty).

        If both request and response are
        empty, the connection establishment alone will indicate health. The request
        data can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#request GoogleComputeRegionHealthCheck#request}
        '''
        result = self._values.get("request")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''The bytes to match against the beginning of the response data.

        If left empty
        (the default value), any response will indicate health. The response data
        can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#response GoogleComputeRegionHealthCheck#response}
        '''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionHealthCheckTcpHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionHealthCheckTcpHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckTcpHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ece1d4c002299f76799d1a18576838249158342b208b5bbceb72fc9a51aa8de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPortName")
    def reset_port_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortName", []))

    @jsii.member(jsii_name="resetPortSpecification")
    def reset_port_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortSpecification", []))

    @jsii.member(jsii_name="resetProxyHeader")
    def reset_proxy_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyHeader", []))

    @jsii.member(jsii_name="resetRequest")
    def reset_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequest", []))

    @jsii.member(jsii_name="resetResponse")
    def reset_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponse", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="portNameInput")
    def port_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portNameInput"))

    @builtins.property
    @jsii.member(jsii_name="portSpecificationInput")
    def port_specification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portSpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyHeaderInput")
    def proxy_header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="requestInput")
    def request_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestInput"))

    @builtins.property
    @jsii.member(jsii_name="responseInput")
    def response_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f031586684f868a9d829e44a1439503e4d062d1e4bcb9ead0d6ac6ee5ea9ee8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3024c0fd25f970a67f1c2cf9af71f1248a7e306bd2775de9b893f73fe0351ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c5c9ca0aa76d638de1a484b610d5bbe1466bd92da8778dc92ad2a58c397f9f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyHeader")
    def proxy_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyHeader"))

    @proxy_header.setter
    def proxy_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9783f420a8feeef7ecd05881f71ac4fda98625520edb4d230516885455ba75d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="request")
    def request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "request"))

    @request.setter
    def request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d8f8cd2ab87fbf1dc12d27a56e968e36cfdc76a1e73fb399f2c429c9c4def0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "request", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd858e529cbabceacb6038360e07b2f208a9f6ebdb3cfc2d1aea89ba46bc5197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionHealthCheckTcpHealthCheck]:
        return typing.cast(typing.Optional[GoogleComputeRegionHealthCheckTcpHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionHealthCheckTcpHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b778baf564d169834d18169cef0a4fa350bbd63076a9965afe0c801a9863bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeRegionHealthCheckTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#create GoogleComputeRegionHealthCheck#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#delete GoogleComputeRegionHealthCheck#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#update GoogleComputeRegionHealthCheck#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1a5d6c9bf980e9c56a6c1575d81d4aaf4c57a46fd610e8184ba0fdfcef0fc0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#create GoogleComputeRegionHealthCheck#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#delete GoogleComputeRegionHealthCheck#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_health_check#update GoogleComputeRegionHealthCheck#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionHealthCheckTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionHealthCheckTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionHealthCheck.GoogleComputeRegionHealthCheckTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c38c7e3c2dabd435d233d8f095b7bddc4463612d8c3b8e389ad240a79d92816)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d7a9eade49503bedd99eb16557a1a5dfeced9e47673a3a99c9dbfac389d9fbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b558a4d953e8edc5543dc0512c8c81e8f1bfd39e877209ed5519193706c7b80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b13242c0e6cb98b971c2736dec31694ad2b47d6846d3e206016e74adeb85dd0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionHealthCheckTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionHealthCheckTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionHealthCheckTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42767bc6ced5dd08e31852d18686d5d6aa2139b2c8d47e4e8a26c1e0ae958539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeRegionHealthCheck",
    "GoogleComputeRegionHealthCheckConfig",
    "GoogleComputeRegionHealthCheckGrpcHealthCheck",
    "GoogleComputeRegionHealthCheckGrpcHealthCheckOutputReference",
    "GoogleComputeRegionHealthCheckGrpcTlsHealthCheck",
    "GoogleComputeRegionHealthCheckGrpcTlsHealthCheckOutputReference",
    "GoogleComputeRegionHealthCheckHttp2HealthCheck",
    "GoogleComputeRegionHealthCheckHttp2HealthCheckOutputReference",
    "GoogleComputeRegionHealthCheckHttpHealthCheck",
    "GoogleComputeRegionHealthCheckHttpHealthCheckOutputReference",
    "GoogleComputeRegionHealthCheckHttpsHealthCheck",
    "GoogleComputeRegionHealthCheckHttpsHealthCheckOutputReference",
    "GoogleComputeRegionHealthCheckLogConfig",
    "GoogleComputeRegionHealthCheckLogConfigOutputReference",
    "GoogleComputeRegionHealthCheckSslHealthCheck",
    "GoogleComputeRegionHealthCheckSslHealthCheckOutputReference",
    "GoogleComputeRegionHealthCheckTcpHealthCheck",
    "GoogleComputeRegionHealthCheckTcpHealthCheckOutputReference",
    "GoogleComputeRegionHealthCheckTimeouts",
    "GoogleComputeRegionHealthCheckTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__bcc3e4120bbbab4f16f445b03fe771b23ad48b3bc355fadb5379c538901d442a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    check_interval_sec: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    grpc_health_check: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckGrpcHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_tls_health_check: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckGrpcTlsHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    healthy_threshold: typing.Optional[jsii.Number] = None,
    http2_health_check: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckHttp2HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    http_health_check: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckHttpHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    https_health_check: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckHttpsHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    ssl_health_check: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckSslHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    tcp_health_check: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckTcpHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_sec: typing.Optional[jsii.Number] = None,
    unhealthy_threshold: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__9f46ef04a3182679c9fd2f467182ebea1a74b390768e9968e1f1a0356d69bc85(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633a6d696240d1392ca45800ff4505968af3e5df81f2ebb2e841d22ae8d8177c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71cbd6a1ea68092628cbb5170925fa6a360f6648748e1bb4f628b7bff38a67b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__992563d2e5772eead30b76d41b6d9c244e670afbdf240b04059ee46b0f439dd0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c80850723679860413dd4c4185d7508d1ea83ba1533f4f2ddd370ceb7e1205(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc26410f3ae76bff886ba2e690ec155726cbf2cd07850a3afa40afb794666e54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057587284a800be6e679fadc550043f3cb82e6bf5a24834ac3e2c22e58734a17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1756fa9cef8cb8266b5b0ad3a345030149e2216eee030e270b8d8b0ffafb7438(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f120090f298a3c7573db92265e155bab49e75e22a4bfb5a86aa4ad3f6e7805d2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9792baaf02e39fea03d980600a1a56a0d9d5bf41b247a348344c984c72e141c1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbea1cfc70fa55017169580102f017663d376074feda6f532aab0ff2e514c25d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    check_interval_sec: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    grpc_health_check: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckGrpcHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_tls_health_check: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckGrpcTlsHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    healthy_threshold: typing.Optional[jsii.Number] = None,
    http2_health_check: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckHttp2HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    http_health_check: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckHttpHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    https_health_check: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckHttpsHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    ssl_health_check: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckSslHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    tcp_health_check: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckTcpHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeRegionHealthCheckTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_sec: typing.Optional[jsii.Number] = None,
    unhealthy_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3edbd700a76959587bce69411dd7995a3683c595b4fe36c5e1e66f05b07193(
    *,
    grpc_service_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    port_name: typing.Optional[builtins.str] = None,
    port_specification: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a1f2c57786f918bc8783fb00c98a64b39c023171cada940083d5cda98d2cba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0facb01a9262a1c87a7f8def380689a0b80375c32437665696220fbcd0996f74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ece6fa826407e7309bc95c2638b7e98299c13ce09be7009f0b9920bbb688228(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab266b6be5d8634b4f85d753facb4021222b3638a38fefb29862a1b31b2cf57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a19332f85ac499c5bb61595b09ee8397c4a8e418e54e6cb9dbafd9497986575(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9d8bc276959a5884396b21cf4b18816b833166693c7924ed6482b9197776bae(
    value: typing.Optional[GoogleComputeRegionHealthCheckGrpcHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee93a470e7cc52d2bbfbd6ce0bdbaf730f1e77ff7fb25dcb3655acdb90afd20(
    *,
    grpc_service_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    port_specification: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6bbb065315d943996fa1fb06244b6da0a9d70c0e2d442563107722e7b606c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7167b97c78387ced69d04df31809e423e9065e3f1eec6344e7373f3fecdd074e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7eb7155e5401a741713100f224d0b767a0a8f72b3430efc3322c38831200ab4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f5dc4a64ca0d0ef4d84884923839dd7d950dbccb78291611bde1dc277d6b08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff77872a3c1e7061fbe80391cddaff1c03e6a7b79e51b3084ea8548faf022107(
    value: typing.Optional[GoogleComputeRegionHealthCheckGrpcTlsHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69c1a7a30de92f4d76051549cd05e8291773164f7c7bf9c6883774643e95aec(
    *,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    port_name: typing.Optional[builtins.str] = None,
    port_specification: typing.Optional[builtins.str] = None,
    proxy_header: typing.Optional[builtins.str] = None,
    request_path: typing.Optional[builtins.str] = None,
    response: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589a4914b26bd51936f0a003748f6d940f081d949febd66b62b23679b3074532(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddf1c0170bb487e7d9d7010851e16f1eb32b71233099a190674fc22a4985f51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1af4edddfec0da1a038e760ad52ed772f2abe95f4e6739f1c7a08607dd61e41(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b17af42a6113585668b7e09d822075f49d0f7b5b427b29b604f22cf95b76c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78af8a811e31cf3fedfe0dcabe9221549078941af3062146158aaa2b7a641eb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907981b9596219f8b73a1c6028d3a90e01ede4109788663a08ffce4e61f05a50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0969bb83e83d64a10761a65fd50640ce4d8c5293a6241da0dc59fb1c1da474(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4048304e7ac3576608083e51df7f28da0fdf70c3b5e3b0a9aa3454d8b6cb801(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c82e100a2f3d3d48b5911d49b16837726d3f83d962e8d4ba8f132653727e4ff(
    value: typing.Optional[GoogleComputeRegionHealthCheckHttp2HealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81fba5e77cb9831e91926eee942526364f18135ad0d826013f809fdd37371848(
    *,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    port_name: typing.Optional[builtins.str] = None,
    port_specification: typing.Optional[builtins.str] = None,
    proxy_header: typing.Optional[builtins.str] = None,
    request_path: typing.Optional[builtins.str] = None,
    response: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5912fb352990ef0e6dc9e3ac195962392cc2956e9b0558878df069d899ee7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62989391614d3c778fc99ea621034ee6c82bc714b422a9aaac2665fe6e831c8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fad2d14b52e72c82cda54721bc2e12b222f60244fc6993b7784231ca01c062f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19bf954a5fb2843f5544fa61805c0f79c52fc3cf03f6f55d49959341a6460b9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844bd009bb620a03887789056ab7e70a4d0a3ed9bce4e9781dbc6716522a422f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a824ded576cfda3feda43249c3a7b1b460c8fa6d8f9aa02f083262caac92901(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__534f2a6be61fc1b08793f440502e368ac5744cc0aba4617f95f64d107ded80aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9eae331a80db55dddd9169f273ea193f906661c3c51c462303ca7aa40fc10d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94b0c47b75e5adb69c9afee400dd5ea9460db72d375d51ff686e1de5790dd39(
    value: typing.Optional[GoogleComputeRegionHealthCheckHttpHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224bcc7e58670676a4abb26812c3477d991a91897988867c03d0f00f99442cd4(
    *,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    port_name: typing.Optional[builtins.str] = None,
    port_specification: typing.Optional[builtins.str] = None,
    proxy_header: typing.Optional[builtins.str] = None,
    request_path: typing.Optional[builtins.str] = None,
    response: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3648df0f32789244d2a6268d8568aae9c6b0ca72f44854b9c465b390e6e39dcd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f28d47099aed11df8fffb242a15a44abf79574c453d0cb7e9a66087dec6faee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0778e188d7848764e23fd600752aa7b76d8fe3eef3969fed023b1b8995bf66a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda69792a9022b0db5202e0fa0b08ec2c54ad0c5c66926770b6e758e8794cad9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece668167637bd0ea53b50e3bf14d5538dff623072c64f98f5e42c232f4cbe02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da15a126b8dfcef4eac107fd23dab4dd23c88b1fa6092850ff838ee508eec5c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64c607ebd62fe7cee7775d5a84f7f5a91d796427b83775fb7b987897992c5e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846efc491a2040a786b51bfe50d568f65e8c682c6033db5a4a6bcf15e434101d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be2d2d1bc1f189eb4643bdf49b6d9fe3d92b036e1b0932bd00d40e26b8d12a4e(
    value: typing.Optional[GoogleComputeRegionHealthCheckHttpsHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c850f00d1d35fa87a60c6392e6087a8ce9bdc8691399db0e351cdc0a1b64342(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bbe9beeea1caffcd43313b10253fe074e958e91ddee499731c915cf42f3c24e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35048e9a9b88cb4881b1f30fe7eb96830b933bb85f830e4bcb2a4735aefefbf5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3d9b54c2a44c9a12bbe0638c34cdf50b0714cab7e8353f4b9843dd429a5df2(
    value: typing.Optional[GoogleComputeRegionHealthCheckLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9111b4cae3cdda47160d40c3ba5b33da79f94a91dc692250f598e7f2638336a6(
    *,
    port: typing.Optional[jsii.Number] = None,
    port_name: typing.Optional[builtins.str] = None,
    port_specification: typing.Optional[builtins.str] = None,
    proxy_header: typing.Optional[builtins.str] = None,
    request: typing.Optional[builtins.str] = None,
    response: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0170f44f2b3a341549f5aab8174f4dc4050857c6533c03e2c57d3472500530c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43841606de3ca3999d442124ba96e1243569c54d4b0481c9014267188bb77f19(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef30335c9b7f1df9ab144765b99856c41dd0e22947fb6c76d8cb85b6b7aed071(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ab92ded1b56ef3fe9134d0825cc5e26582365f5dcde68638c85c4715a5bb70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2751e1c13276969e4b5e7e17741e5338ea5510259062012a8f440305bb0f709d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53457507b5e8c2b8c29d8300b1c1552a49ccf7a072cae9b8c71aab74182ebf7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fad0a60846b969c65184b5cf0e0a2404556aa6f3438ca2514ab423c5149e153(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d86f9f22ec2bf170e076bb6707e2d87b8d477c9103fc3ac401bfaf035efad736(
    value: typing.Optional[GoogleComputeRegionHealthCheckSslHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430c9756617ec319eafbb587da46878fb1626a76638d2af2f332ed12118494cf(
    *,
    port: typing.Optional[jsii.Number] = None,
    port_name: typing.Optional[builtins.str] = None,
    port_specification: typing.Optional[builtins.str] = None,
    proxy_header: typing.Optional[builtins.str] = None,
    request: typing.Optional[builtins.str] = None,
    response: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ece1d4c002299f76799d1a18576838249158342b208b5bbceb72fc9a51aa8de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f031586684f868a9d829e44a1439503e4d062d1e4bcb9ead0d6ac6ee5ea9ee8e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3024c0fd25f970a67f1c2cf9af71f1248a7e306bd2775de9b893f73fe0351ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5c9ca0aa76d638de1a484b610d5bbe1466bd92da8778dc92ad2a58c397f9f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9783f420a8feeef7ecd05881f71ac4fda98625520edb4d230516885455ba75d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d8f8cd2ab87fbf1dc12d27a56e968e36cfdc76a1e73fb399f2c429c9c4def0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd858e529cbabceacb6038360e07b2f208a9f6ebdb3cfc2d1aea89ba46bc5197(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b778baf564d169834d18169cef0a4fa350bbd63076a9965afe0c801a9863bcb(
    value: typing.Optional[GoogleComputeRegionHealthCheckTcpHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1a5d6c9bf980e9c56a6c1575d81d4aaf4c57a46fd610e8184ba0fdfcef0fc0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c38c7e3c2dabd435d233d8f095b7bddc4463612d8c3b8e389ad240a79d92816(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7a9eade49503bedd99eb16557a1a5dfeced9e47673a3a99c9dbfac389d9fbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b558a4d953e8edc5543dc0512c8c81e8f1bfd39e877209ed5519193706c7b80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b13242c0e6cb98b971c2736dec31694ad2b47d6846d3e206016e74adeb85dd0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42767bc6ced5dd08e31852d18686d5d6aa2139b2c8d47e4e8a26c1e0ae958539(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionHealthCheckTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
