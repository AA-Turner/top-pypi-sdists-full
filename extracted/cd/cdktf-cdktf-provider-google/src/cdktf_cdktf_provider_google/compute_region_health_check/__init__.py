r'''
# `google_compute_region_health_check`

Refer to the Terraform Registry for docs: [`google_compute_region_health_check`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check).
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


class ComputeRegionHealthCheck(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheck",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check google_compute_region_health_check}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        check_interval_sec: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        grpc_health_check: typing.Optional[typing.Union["ComputeRegionHealthCheckGrpcHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        healthy_threshold: typing.Optional[jsii.Number] = None,
        http2_health_check: typing.Optional[typing.Union["ComputeRegionHealthCheckHttp2HealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        http_health_check: typing.Optional[typing.Union["ComputeRegionHealthCheckHttpHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        https_health_check: typing.Optional[typing.Union["ComputeRegionHealthCheckHttpsHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["ComputeRegionHealthCheckLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        ssl_health_check: typing.Optional[typing.Union["ComputeRegionHealthCheckSslHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        tcp_health_check: typing.Optional[typing.Union["ComputeRegionHealthCheckTcpHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionHealthCheckTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check google_compute_region_health_check} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#name ComputeRegionHealthCheck#name}
        :param check_interval_sec: How often (in seconds) to send a health check. The default value is 5 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#check_interval_sec ComputeRegionHealthCheck#check_interval_sec}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#description ComputeRegionHealthCheck#description}
        :param grpc_health_check: grpc_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#grpc_health_check ComputeRegionHealthCheck#grpc_health_check}
        :param healthy_threshold: A so-far unhealthy instance will be marked healthy after this many consecutive successes. The default value is 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#healthy_threshold ComputeRegionHealthCheck#healthy_threshold}
        :param http2_health_check: http2_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#http2_health_check ComputeRegionHealthCheck#http2_health_check}
        :param http_health_check: http_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#http_health_check ComputeRegionHealthCheck#http_health_check}
        :param https_health_check: https_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#https_health_check ComputeRegionHealthCheck#https_health_check}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#id ComputeRegionHealthCheck#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#log_config ComputeRegionHealthCheck#log_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#project ComputeRegionHealthCheck#project}.
        :param region: The Region in which the created health check should reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#region ComputeRegionHealthCheck#region}
        :param ssl_health_check: ssl_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#ssl_health_check ComputeRegionHealthCheck#ssl_health_check}
        :param tcp_health_check: tcp_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#tcp_health_check ComputeRegionHealthCheck#tcp_health_check}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#timeouts ComputeRegionHealthCheck#timeouts}
        :param timeout_sec: How long (in seconds) to wait before claiming failure. The default value is 5 seconds. It is invalid for timeoutSec to have greater value than checkIntervalSec. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#timeout_sec ComputeRegionHealthCheck#timeout_sec}
        :param unhealthy_threshold: A so-far healthy instance will be marked unhealthy after this many consecutive failures. The default value is 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#unhealthy_threshold ComputeRegionHealthCheck#unhealthy_threshold}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a17996944d215ea73d175d44dc4c0b0a01794a871223e69a62a12d470b8a8695)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRegionHealthCheckConfig(
            name=name,
            check_interval_sec=check_interval_sec,
            description=description,
            grpc_health_check=grpc_health_check,
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
        '''Generates CDKTF code for importing a ComputeRegionHealthCheck resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRegionHealthCheck to import.
        :param import_from_id: The id of the existing ComputeRegionHealthCheck that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRegionHealthCheck to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2813e8798cf0d6d4e9af4620aff0a106b67c0490897ad6971847b367240e93)
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
        :param grpc_service_name: The gRPC service name for the health check. The value of grpcServiceName has the following meanings by convention:. - Empty serviceName means the overall status of all services at the backend. - Non-empty serviceName means the health of that gRPC service, as defined by the owner of the service. The grpcServiceName can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#grpc_service_name ComputeRegionHealthCheck#grpc_service_name}
        :param port: The port number for the health check request. Must be specified if portName and portSpecification are not set or if port_specification is USE_FIXED_PORT. Valid values are 1 through 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, gRPC health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        '''
        value = ComputeRegionHealthCheckGrpcHealthCheck(
            grpc_service_name=grpc_service_name,
            port=port,
            port_name=port_name,
            port_specification=port_specification,
        )

        return typing.cast(None, jsii.invoke(self, "putGrpcHealthCheck", [value]))

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
        :param host: The value of the host header in the HTTP2 health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#host ComputeRegionHealthCheck#host}
        :param port: The TCP port number for the HTTP2 health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTP2 health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#proxy_header ComputeRegionHealthCheck#proxy_header}
        :param request_path: The request path of the HTTP2 health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#request_path ComputeRegionHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#response ComputeRegionHealthCheck#response}
        '''
        value = ComputeRegionHealthCheckHttp2HealthCheck(
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
        :param host: The value of the host header in the HTTP health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#host ComputeRegionHealthCheck#host}
        :param port: The TCP port number for the HTTP health check request. The default value is 80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTP health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#proxy_header ComputeRegionHealthCheck#proxy_header}
        :param request_path: The request path of the HTTP health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#request_path ComputeRegionHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#response ComputeRegionHealthCheck#response}
        '''
        value = ComputeRegionHealthCheckHttpHealthCheck(
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
        :param host: The value of the host header in the HTTPS health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#host ComputeRegionHealthCheck#host}
        :param port: The TCP port number for the HTTPS health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTPS health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#proxy_header ComputeRegionHealthCheck#proxy_header}
        :param request_path: The request path of the HTTPS health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#request_path ComputeRegionHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#response ComputeRegionHealthCheck#response}
        '''
        value = ComputeRegionHealthCheckHttpsHealthCheck(
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
        :param enable: Indicates whether or not to export logs. This is false by default, which means no health check logging will be done. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#enable ComputeRegionHealthCheck#enable}
        '''
        value = ComputeRegionHealthCheckLogConfig(enable=enable)

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
        :param port: The TCP port number for the SSL health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, SSL health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#proxy_header ComputeRegionHealthCheck#proxy_header}
        :param request: The application data to send once the SSL connection has been established (default value is empty). If both request and response are empty, the connection establishment alone will indicate health. The request data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#request ComputeRegionHealthCheck#request}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#response ComputeRegionHealthCheck#response}
        '''
        value = ComputeRegionHealthCheckSslHealthCheck(
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
        :param port: The TCP port number for the TCP health check request. The default value is 80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, TCP health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#proxy_header ComputeRegionHealthCheck#proxy_header}
        :param request: The application data to send once the TCP connection has been established (default value is empty). If both request and response are empty, the connection establishment alone will indicate health. The request data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#request ComputeRegionHealthCheck#request}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#response ComputeRegionHealthCheck#response}
        '''
        value = ComputeRegionHealthCheckTcpHealthCheck(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#create ComputeRegionHealthCheck#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#delete ComputeRegionHealthCheck#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#update ComputeRegionHealthCheck#update}.
        '''
        value = ComputeRegionHealthCheckTimeouts(
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
    ) -> "ComputeRegionHealthCheckGrpcHealthCheckOutputReference":
        return typing.cast("ComputeRegionHealthCheckGrpcHealthCheckOutputReference", jsii.get(self, "grpcHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckId")
    def health_check_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthCheckId"))

    @builtins.property
    @jsii.member(jsii_name="http2HealthCheck")
    def http2_health_check(
        self,
    ) -> "ComputeRegionHealthCheckHttp2HealthCheckOutputReference":
        return typing.cast("ComputeRegionHealthCheckHttp2HealthCheckOutputReference", jsii.get(self, "http2HealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="httpHealthCheck")
    def http_health_check(
        self,
    ) -> "ComputeRegionHealthCheckHttpHealthCheckOutputReference":
        return typing.cast("ComputeRegionHealthCheckHttpHealthCheckOutputReference", jsii.get(self, "httpHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="httpsHealthCheck")
    def https_health_check(
        self,
    ) -> "ComputeRegionHealthCheckHttpsHealthCheckOutputReference":
        return typing.cast("ComputeRegionHealthCheckHttpsHealthCheckOutputReference", jsii.get(self, "httpsHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="logConfig")
    def log_config(self) -> "ComputeRegionHealthCheckLogConfigOutputReference":
        return typing.cast("ComputeRegionHealthCheckLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="sslHealthCheck")
    def ssl_health_check(
        self,
    ) -> "ComputeRegionHealthCheckSslHealthCheckOutputReference":
        return typing.cast("ComputeRegionHealthCheckSslHealthCheckOutputReference", jsii.get(self, "sslHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="tcpHealthCheck")
    def tcp_health_check(
        self,
    ) -> "ComputeRegionHealthCheckTcpHealthCheckOutputReference":
        return typing.cast("ComputeRegionHealthCheckTcpHealthCheckOutputReference", jsii.get(self, "tcpHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeRegionHealthCheckTimeoutsOutputReference":
        return typing.cast("ComputeRegionHealthCheckTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["ComputeRegionHealthCheckGrpcHealthCheck"]:
        return typing.cast(typing.Optional["ComputeRegionHealthCheckGrpcHealthCheck"], jsii.get(self, "grpcHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="healthyThresholdInput")
    def healthy_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthyThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="http2HealthCheckInput")
    def http2_health_check_input(
        self,
    ) -> typing.Optional["ComputeRegionHealthCheckHttp2HealthCheck"]:
        return typing.cast(typing.Optional["ComputeRegionHealthCheckHttp2HealthCheck"], jsii.get(self, "http2HealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHealthCheckInput")
    def http_health_check_input(
        self,
    ) -> typing.Optional["ComputeRegionHealthCheckHttpHealthCheck"]:
        return typing.cast(typing.Optional["ComputeRegionHealthCheckHttpHealthCheck"], jsii.get(self, "httpHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsHealthCheckInput")
    def https_health_check_input(
        self,
    ) -> typing.Optional["ComputeRegionHealthCheckHttpsHealthCheck"]:
        return typing.cast(typing.Optional["ComputeRegionHealthCheckHttpsHealthCheck"], jsii.get(self, "httpsHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigInput")
    def log_config_input(self) -> typing.Optional["ComputeRegionHealthCheckLogConfig"]:
        return typing.cast(typing.Optional["ComputeRegionHealthCheckLogConfig"], jsii.get(self, "logConfigInput"))

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
    ) -> typing.Optional["ComputeRegionHealthCheckSslHealthCheck"]:
        return typing.cast(typing.Optional["ComputeRegionHealthCheckSslHealthCheck"], jsii.get(self, "sslHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpHealthCheckInput")
    def tcp_health_check_input(
        self,
    ) -> typing.Optional["ComputeRegionHealthCheckTcpHealthCheck"]:
        return typing.cast(typing.Optional["ComputeRegionHealthCheckTcpHealthCheck"], jsii.get(self, "tcpHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecInput")
    def timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionHealthCheckTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionHealthCheckTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e3f43706ea46a596554690b7d753d38ad5cd656046c5bf234a0660f826cb2ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkIntervalSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74273865dd2abfaff6f346f5d3b0c55f2492f405a19b783bcf716a24ad75fb4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthyThreshold")
    def healthy_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthyThreshold"))

    @healthy_threshold.setter
    def healthy_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17e50026daaef5bfd2eeb4559dd726f0ce1a14551ed2b4766b0da517e96370ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthyThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de681bc2db2c5ff0538a05f5f4a94bb7d6d85b86d38bd138c590a688f14b22f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1520e2c2421c67685463bcf5eb7c71a808f3cb8ef563429c707747340159e1a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa109ddf461422f453020be09ded075667419c202be277fc6074ce99582b8284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a35ede31ceb484a5832d93168f02eb4dfde246ed79edb0f86b177d89ffa4f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSec")
    def timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSec"))

    @timeout_sec.setter
    def timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc59790d798377ea7bd566f5d6bd59129c8b7cb41000197edde3eed11a35d8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unhealthyThreshold")
    def unhealthy_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unhealthyThreshold"))

    @unhealthy_threshold.setter
    def unhealthy_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb1b31cf9e052798bde1a398e0dcb5cad79d210a65ffdbd56fffc3f5c9359aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unhealthyThreshold", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckConfig",
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
class ComputeRegionHealthCheckConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        grpc_health_check: typing.Optional[typing.Union["ComputeRegionHealthCheckGrpcHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        healthy_threshold: typing.Optional[jsii.Number] = None,
        http2_health_check: typing.Optional[typing.Union["ComputeRegionHealthCheckHttp2HealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        http_health_check: typing.Optional[typing.Union["ComputeRegionHealthCheckHttpHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        https_health_check: typing.Optional[typing.Union["ComputeRegionHealthCheckHttpsHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["ComputeRegionHealthCheckLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        ssl_health_check: typing.Optional[typing.Union["ComputeRegionHealthCheckSslHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        tcp_health_check: typing.Optional[typing.Union["ComputeRegionHealthCheckTcpHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionHealthCheckTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#name ComputeRegionHealthCheck#name}
        :param check_interval_sec: How often (in seconds) to send a health check. The default value is 5 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#check_interval_sec ComputeRegionHealthCheck#check_interval_sec}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#description ComputeRegionHealthCheck#description}
        :param grpc_health_check: grpc_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#grpc_health_check ComputeRegionHealthCheck#grpc_health_check}
        :param healthy_threshold: A so-far unhealthy instance will be marked healthy after this many consecutive successes. The default value is 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#healthy_threshold ComputeRegionHealthCheck#healthy_threshold}
        :param http2_health_check: http2_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#http2_health_check ComputeRegionHealthCheck#http2_health_check}
        :param http_health_check: http_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#http_health_check ComputeRegionHealthCheck#http_health_check}
        :param https_health_check: https_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#https_health_check ComputeRegionHealthCheck#https_health_check}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#id ComputeRegionHealthCheck#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#log_config ComputeRegionHealthCheck#log_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#project ComputeRegionHealthCheck#project}.
        :param region: The Region in which the created health check should reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#region ComputeRegionHealthCheck#region}
        :param ssl_health_check: ssl_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#ssl_health_check ComputeRegionHealthCheck#ssl_health_check}
        :param tcp_health_check: tcp_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#tcp_health_check ComputeRegionHealthCheck#tcp_health_check}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#timeouts ComputeRegionHealthCheck#timeouts}
        :param timeout_sec: How long (in seconds) to wait before claiming failure. The default value is 5 seconds. It is invalid for timeoutSec to have greater value than checkIntervalSec. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#timeout_sec ComputeRegionHealthCheck#timeout_sec}
        :param unhealthy_threshold: A so-far healthy instance will be marked unhealthy after this many consecutive failures. The default value is 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#unhealthy_threshold ComputeRegionHealthCheck#unhealthy_threshold}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(grpc_health_check, dict):
            grpc_health_check = ComputeRegionHealthCheckGrpcHealthCheck(**grpc_health_check)
        if isinstance(http2_health_check, dict):
            http2_health_check = ComputeRegionHealthCheckHttp2HealthCheck(**http2_health_check)
        if isinstance(http_health_check, dict):
            http_health_check = ComputeRegionHealthCheckHttpHealthCheck(**http_health_check)
        if isinstance(https_health_check, dict):
            https_health_check = ComputeRegionHealthCheckHttpsHealthCheck(**https_health_check)
        if isinstance(log_config, dict):
            log_config = ComputeRegionHealthCheckLogConfig(**log_config)
        if isinstance(ssl_health_check, dict):
            ssl_health_check = ComputeRegionHealthCheckSslHealthCheck(**ssl_health_check)
        if isinstance(tcp_health_check, dict):
            tcp_health_check = ComputeRegionHealthCheckTcpHealthCheck(**tcp_health_check)
        if isinstance(timeouts, dict):
            timeouts = ComputeRegionHealthCheckTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb251f0cde36d33e9e03f48f1a3b0d90679bfe39f92fd72d5f33f957e87fdaa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#name ComputeRegionHealthCheck#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def check_interval_sec(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to send a health check. The default value is 5 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#check_interval_sec ComputeRegionHealthCheck#check_interval_sec}
        '''
        result = self._values.get("check_interval_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#description ComputeRegionHealthCheck#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grpc_health_check(
        self,
    ) -> typing.Optional["ComputeRegionHealthCheckGrpcHealthCheck"]:
        '''grpc_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#grpc_health_check ComputeRegionHealthCheck#grpc_health_check}
        '''
        result = self._values.get("grpc_health_check")
        return typing.cast(typing.Optional["ComputeRegionHealthCheckGrpcHealthCheck"], result)

    @builtins.property
    def healthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''A so-far unhealthy instance will be marked healthy after this many consecutive successes. The default value is 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#healthy_threshold ComputeRegionHealthCheck#healthy_threshold}
        '''
        result = self._values.get("healthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def http2_health_check(
        self,
    ) -> typing.Optional["ComputeRegionHealthCheckHttp2HealthCheck"]:
        '''http2_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#http2_health_check ComputeRegionHealthCheck#http2_health_check}
        '''
        result = self._values.get("http2_health_check")
        return typing.cast(typing.Optional["ComputeRegionHealthCheckHttp2HealthCheck"], result)

    @builtins.property
    def http_health_check(
        self,
    ) -> typing.Optional["ComputeRegionHealthCheckHttpHealthCheck"]:
        '''http_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#http_health_check ComputeRegionHealthCheck#http_health_check}
        '''
        result = self._values.get("http_health_check")
        return typing.cast(typing.Optional["ComputeRegionHealthCheckHttpHealthCheck"], result)

    @builtins.property
    def https_health_check(
        self,
    ) -> typing.Optional["ComputeRegionHealthCheckHttpsHealthCheck"]:
        '''https_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#https_health_check ComputeRegionHealthCheck#https_health_check}
        '''
        result = self._values.get("https_health_check")
        return typing.cast(typing.Optional["ComputeRegionHealthCheckHttpsHealthCheck"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#id ComputeRegionHealthCheck#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_config(self) -> typing.Optional["ComputeRegionHealthCheckLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#log_config ComputeRegionHealthCheck#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["ComputeRegionHealthCheckLogConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#project ComputeRegionHealthCheck#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The Region in which the created health check should reside. If it is not provided, the provider region is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#region ComputeRegionHealthCheck#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_health_check(
        self,
    ) -> typing.Optional["ComputeRegionHealthCheckSslHealthCheck"]:
        '''ssl_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#ssl_health_check ComputeRegionHealthCheck#ssl_health_check}
        '''
        result = self._values.get("ssl_health_check")
        return typing.cast(typing.Optional["ComputeRegionHealthCheckSslHealthCheck"], result)

    @builtins.property
    def tcp_health_check(
        self,
    ) -> typing.Optional["ComputeRegionHealthCheckTcpHealthCheck"]:
        '''tcp_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#tcp_health_check ComputeRegionHealthCheck#tcp_health_check}
        '''
        result = self._values.get("tcp_health_check")
        return typing.cast(typing.Optional["ComputeRegionHealthCheckTcpHealthCheck"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeRegionHealthCheckTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#timeouts ComputeRegionHealthCheck#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRegionHealthCheckTimeouts"], result)

    @builtins.property
    def timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''How long (in seconds) to wait before claiming failure.

        The default value is 5 seconds.  It is invalid for timeoutSec to have
        greater value than checkIntervalSec.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#timeout_sec ComputeRegionHealthCheck#timeout_sec}
        '''
        result = self._values.get("timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''A so-far healthy instance will be marked unhealthy after this many consecutive failures. The default value is 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#unhealthy_threshold ComputeRegionHealthCheck#unhealthy_threshold}
        '''
        result = self._values.get("unhealthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionHealthCheckConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckGrpcHealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "grpc_service_name": "grpcServiceName",
        "port": "port",
        "port_name": "portName",
        "port_specification": "portSpecification",
    },
)
class ComputeRegionHealthCheckGrpcHealthCheck:
    def __init__(
        self,
        *,
        grpc_service_name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        port_name: typing.Optional[builtins.str] = None,
        port_specification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param grpc_service_name: The gRPC service name for the health check. The value of grpcServiceName has the following meanings by convention:. - Empty serviceName means the overall status of all services at the backend. - Non-empty serviceName means the health of that gRPC service, as defined by the owner of the service. The grpcServiceName can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#grpc_service_name ComputeRegionHealthCheck#grpc_service_name}
        :param port: The port number for the health check request. Must be specified if portName and portSpecification are not set or if port_specification is USE_FIXED_PORT. Valid values are 1 through 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, gRPC health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a82c5465465f3aa672866eea82dcad697d6b42d6288ab0cba0b79a700a18d4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#grpc_service_name ComputeRegionHealthCheck#grpc_service_name}
        '''
        result = self._values.get("grpc_service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port number for the health check request.

        Must be specified if portName and portSpecification are not set
        or if port_specification is USE_FIXED_PORT. Valid values are 1 through 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionHealthCheckGrpcHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionHealthCheckGrpcHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckGrpcHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c04e949b149ddf11b83b8a64dae7f559f1c40954db400f4f9eeb7f9123706850)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e36cd381e55f3dfa091d22ebd1d7f7e66e8fc98bc7a2431f6ea814a5a19760c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grpcServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c26420a09ef5849142989ec09e896861744599c0050c998c6bb3a09fc8fcbed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__351066719bbb2f4ef1d125786c3f85a602dcf31447d5d06dd427b60f26751a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55c6ecec21449e4c4443ccdfa8608e04b45f6b3636a58f92936885862199e5b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionHealthCheckGrpcHealthCheck]:
        return typing.cast(typing.Optional[ComputeRegionHealthCheckGrpcHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionHealthCheckGrpcHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716d3b0b156400f0d5b08ea0be0e4a205a4c27aaf84a92e6f0e7f7f319e66660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckHttp2HealthCheck",
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
class ComputeRegionHealthCheckHttp2HealthCheck:
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
        :param host: The value of the host header in the HTTP2 health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#host ComputeRegionHealthCheck#host}
        :param port: The TCP port number for the HTTP2 health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTP2 health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#proxy_header ComputeRegionHealthCheck#proxy_header}
        :param request_path: The request path of the HTTP2 health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#request_path ComputeRegionHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#response ComputeRegionHealthCheck#response}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e59258114bd2afab208627e881548142e81e919c65eb45a069542d44a84001)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#host ComputeRegionHealthCheck#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The TCP port number for the HTTP2 health check request. The default value is 443.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_header(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of proxy header to append before sending data to the backend.

        Default value: "NONE" Possible values: ["NONE", "PROXY_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#proxy_header ComputeRegionHealthCheck#proxy_header}
        '''
        result = self._values.get("proxy_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_path(self) -> typing.Optional[builtins.str]:
        '''The request path of the HTTP2 health check request. The default value is /.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#request_path ComputeRegionHealthCheck#request_path}
        '''
        result = self._values.get("request_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''The bytes to match against the beginning of the response data.

        If left empty
        (the default value), any response will indicate health. The response data
        can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#response ComputeRegionHealthCheck#response}
        '''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionHealthCheckHttp2HealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionHealthCheckHttp2HealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckHttp2HealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a397806b906aeabbb8b82e426a72a2487ec522e15a1212a40d6fa6a853ddb0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c4125ad9c9ed151be62cf9867856052aa6523917217eec1eb310cbd72ea8c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd1a5c06eca2afbb5fa1dd827845836d1c532df1fd3e49088231f36f9fc4c78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b50e84f8445fe93522f8ae157f2af1c12e83edb4b3428ca3a3256d0d301dd06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca36202b388fbc2932f1c5b7c1178a65c514b37373a0a299934342bc96afae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyHeader")
    def proxy_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyHeader"))

    @proxy_header.setter
    def proxy_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a868e44d0cb80deb40567099cb9019b7b471568680ba7b4f7b98be80303f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestPath")
    def request_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestPath"))

    @request_path.setter
    def request_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8795ac1908c9f1ec316d5cdbf6c75cfc7cccced6da489798ffe4fe364c7c2b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b331d80bec721095206957d5f1b09ce622c8e5c6c699f5d67590e02ceeae64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionHealthCheckHttp2HealthCheck]:
        return typing.cast(typing.Optional[ComputeRegionHealthCheckHttp2HealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionHealthCheckHttp2HealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eb165b6cc82a2c95ecbc5e90abc463b09e762830fb02b9ac5379725327c9e74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckHttpHealthCheck",
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
class ComputeRegionHealthCheckHttpHealthCheck:
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
        :param host: The value of the host header in the HTTP health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#host ComputeRegionHealthCheck#host}
        :param port: The TCP port number for the HTTP health check request. The default value is 80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTP health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#proxy_header ComputeRegionHealthCheck#proxy_header}
        :param request_path: The request path of the HTTP health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#request_path ComputeRegionHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#response ComputeRegionHealthCheck#response}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a91a6d0942d41046a007309780b463a91add8c8bb15ea4e4491b51bbf80d8b8b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#host ComputeRegionHealthCheck#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The TCP port number for the HTTP health check request. The default value is 80.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_header(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of proxy header to append before sending data to the backend.

        Default value: "NONE" Possible values: ["NONE", "PROXY_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#proxy_header ComputeRegionHealthCheck#proxy_header}
        '''
        result = self._values.get("proxy_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_path(self) -> typing.Optional[builtins.str]:
        '''The request path of the HTTP health check request. The default value is /.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#request_path ComputeRegionHealthCheck#request_path}
        '''
        result = self._values.get("request_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''The bytes to match against the beginning of the response data.

        If left empty
        (the default value), any response will indicate health. The response data
        can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#response ComputeRegionHealthCheck#response}
        '''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionHealthCheckHttpHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionHealthCheckHttpHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckHttpHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93eeae04aa25cfbc6e370a9afc66876ea169cde5b9bc9453f9a963d433a4d5e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49d3e87d81522f5771a6ea54a371871ae81bdb3a7f3df074322b581ed1de114e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0615e1df2d43d02d3e0a859933e904472ae73d735cea8ebdc3f2419bbed6c22d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7033f4ef990af71f55ce18f358a47816344c0169b48cc389c0d99734701a5056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5603a7b72bc5a71729f1b5b2468d356d37ac26575278f50075b52bd9797f4cef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyHeader")
    def proxy_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyHeader"))

    @proxy_header.setter
    def proxy_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21914ee92e53241822f9f1f8856374d3bb050fd3629da1974edbe115a373b85e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestPath")
    def request_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestPath"))

    @request_path.setter
    def request_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e0887dd50ca938129cca0655910a828e70221329c6f2e2035185aa4fe56cca6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2156a76e2202739bd7a891b0aa6a68f0479efbe808ae848e00f5f9f05c2959f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionHealthCheckHttpHealthCheck]:
        return typing.cast(typing.Optional[ComputeRegionHealthCheckHttpHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionHealthCheckHttpHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d13e6c3cab6ce35625de785f6fddd9afc2af91d40315aab1691d68cd536c543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckHttpsHealthCheck",
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
class ComputeRegionHealthCheckHttpsHealthCheck:
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
        :param host: The value of the host header in the HTTPS health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#host ComputeRegionHealthCheck#host}
        :param port: The TCP port number for the HTTPS health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTPS health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#proxy_header ComputeRegionHealthCheck#proxy_header}
        :param request_path: The request path of the HTTPS health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#request_path ComputeRegionHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#response ComputeRegionHealthCheck#response}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7067a0396f45a928a5e1157a1fd2a9f7e368ad1a71d6c90ca7a8ca5e6e5805b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#host ComputeRegionHealthCheck#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The TCP port number for the HTTPS health check request. The default value is 443.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_header(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of proxy header to append before sending data to the backend.

        Default value: "NONE" Possible values: ["NONE", "PROXY_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#proxy_header ComputeRegionHealthCheck#proxy_header}
        '''
        result = self._values.get("proxy_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_path(self) -> typing.Optional[builtins.str]:
        '''The request path of the HTTPS health check request. The default value is /.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#request_path ComputeRegionHealthCheck#request_path}
        '''
        result = self._values.get("request_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''The bytes to match against the beginning of the response data.

        If left empty
        (the default value), any response will indicate health. The response data
        can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#response ComputeRegionHealthCheck#response}
        '''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionHealthCheckHttpsHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionHealthCheckHttpsHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckHttpsHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbdb3a491fd0f466eccb700b4d374c970c4203869e4a0879d65d4936d0976d4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e98cda82ab79572404f6e9bbf8718702b9c7bd57743e3a64be381e6d2698a44e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9022dbae48bcf42b5db002f86bb902d9fc1cc82b558859bdec6feb1346cfca66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de5cd01f05a3d2e50f68bc10a8aea92378cde96de1561bc6d22e61bbf3dcb5d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c54483615c013d1913314cc9b44c07f800686bb42e6e55836afc29cf4b51cb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyHeader")
    def proxy_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyHeader"))

    @proxy_header.setter
    def proxy_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05875cb1f9002420e5d84232d8749bc137ed998773a6784085d1cc5837345daf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestPath")
    def request_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestPath"))

    @request_path.setter
    def request_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced151ace3c15628b1a64962faaf1b1a1870c6c4a2c92d8a5ace067308e3ff78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4014488d8281e3d971b28ecd1d3e65d9ec1605cecd3c289a6ae7f57bb5497f6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionHealthCheckHttpsHealthCheck]:
        return typing.cast(typing.Optional[ComputeRegionHealthCheckHttpsHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionHealthCheckHttpsHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8a5b77cb287b18f12a28a1c396fa9a1617ebd790041276b0aadd41781589002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckLogConfig",
    jsii_struct_bases=[],
    name_mapping={"enable": "enable"},
)
class ComputeRegionHealthCheckLogConfig:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable: Indicates whether or not to export logs. This is false by default, which means no health check logging will be done. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#enable ComputeRegionHealthCheck#enable}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468654a1ab5bdc05b9256402cc0b77c68c406cda30340d6d74f87ee9e6ae6e4e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#enable ComputeRegionHealthCheck#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionHealthCheckLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionHealthCheckLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4de01ba316e1a8c7e9f5159625829e8c95804d063e7a283b2cc7bb0155eed43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17e2b8edd5f569338b6889e34efda9bf7acbc83f7fc37cb1672a23e0593760ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRegionHealthCheckLogConfig]:
        return typing.cast(typing.Optional[ComputeRegionHealthCheckLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionHealthCheckLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c816cb983bd47a5600f9df6d99ed2c1fdd66e62285e26788e5e597060e103cf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckSslHealthCheck",
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
class ComputeRegionHealthCheckSslHealthCheck:
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
        :param port: The TCP port number for the SSL health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, SSL health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#proxy_header ComputeRegionHealthCheck#proxy_header}
        :param request: The application data to send once the SSL connection has been established (default value is empty). If both request and response are empty, the connection establishment alone will indicate health. The request data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#request ComputeRegionHealthCheck#request}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#response ComputeRegionHealthCheck#response}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64ca4875db131f37e11bc17f42a978600de6ecc87f8c1fe9768e67f763179d3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_header(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of proxy header to append before sending data to the backend.

        Default value: "NONE" Possible values: ["NONE", "PROXY_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#proxy_header ComputeRegionHealthCheck#proxy_header}
        '''
        result = self._values.get("proxy_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request(self) -> typing.Optional[builtins.str]:
        '''The application data to send once the SSL connection has been established (default value is empty).

        If both request and response are
        empty, the connection establishment alone will indicate health. The request
        data can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#request ComputeRegionHealthCheck#request}
        '''
        result = self._values.get("request")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''The bytes to match against the beginning of the response data.

        If left empty
        (the default value), any response will indicate health. The response data
        can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#response ComputeRegionHealthCheck#response}
        '''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionHealthCheckSslHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionHealthCheckSslHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckSslHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9576d8cc8b0e923d2d1642d0ec4fb3d68f41287033dd7a8ec08cf5e8d0cce35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37780262cd2c84b86bfffa2c0e752794eebaf672ad8c9c4f62758d093a92161b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d053945a0b5f63f4c56b8b94584152b4681d4ea4c955a43676bb288724753ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a80a74166cf28ba8f908e8ecb29bdc1460fa365aea9829a77f97ede5195947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyHeader")
    def proxy_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyHeader"))

    @proxy_header.setter
    def proxy_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce69857a61277410c74097aebd41c0478066f6687db9107d72f66cb0c29d978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="request")
    def request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "request"))

    @request.setter
    def request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74379d53d56679ba65937e2a9f1828a116e1e044800d1c0b39405e820175196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "request", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3ac5de68c22773b01dee8d9f9d0b69c53bfdcfb7a93159d4f02e5b5189aa478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRegionHealthCheckSslHealthCheck]:
        return typing.cast(typing.Optional[ComputeRegionHealthCheckSslHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionHealthCheckSslHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e5824699d09d90669babf5dad282fde0690f5f7a5f7ea5dc0d936575dbb7fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckTcpHealthCheck",
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
class ComputeRegionHealthCheckTcpHealthCheck:
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
        :param port: The TCP port number for the TCP health check request. The default value is 80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, TCP health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#proxy_header ComputeRegionHealthCheck#proxy_header}
        :param request: The application data to send once the TCP connection has been established (default value is empty). If both request and response are empty, the connection establishment alone will indicate health. The request data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#request ComputeRegionHealthCheck#request}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#response ComputeRegionHealthCheck#response}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb1b83d5f084ce34a0b0629ac8551534e956a870a3f873498042f8b168d92fe9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port ComputeRegionHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_name ComputeRegionHealthCheck#port_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#port_specification ComputeRegionHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_header(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of proxy header to append before sending data to the backend.

        Default value: "NONE" Possible values: ["NONE", "PROXY_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#proxy_header ComputeRegionHealthCheck#proxy_header}
        '''
        result = self._values.get("proxy_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request(self) -> typing.Optional[builtins.str]:
        '''The application data to send once the TCP connection has been established (default value is empty).

        If both request and response are
        empty, the connection establishment alone will indicate health. The request
        data can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#request ComputeRegionHealthCheck#request}
        '''
        result = self._values.get("request")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''The bytes to match against the beginning of the response data.

        If left empty
        (the default value), any response will indicate health. The response data
        can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#response ComputeRegionHealthCheck#response}
        '''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionHealthCheckTcpHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionHealthCheckTcpHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckTcpHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92d6fbea4d8225e61040b6f3115907df5eff05468aa9fb66186e9c450980fee2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9516c89ee100318adaeb5fee887c0ee4bf1dec5ef0421ee5fcee3d70333f5c16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37a84def36f1a0fbf290fa87ef5aa83fec0594c5ccecac06f8bb610233fe4d6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7faddeac4abf57f5227e09605e9a8ad61cc9f2c5093d44c1c0d9b56428648f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyHeader")
    def proxy_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyHeader"))

    @proxy_header.setter
    def proxy_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c50c51b75cd659bcb14c966e6da177c8302bb313eab0e1429fe461e874d53af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="request")
    def request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "request"))

    @request.setter
    def request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5675c6ce35e01a40fd28e931c472af7fda2f9a3e5b361fb0d33dabfdc73b46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "request", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27da4ea1dbae99575447f37a38033203f16246b48ee2cd01bf5ad6d3f8fbc9af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRegionHealthCheckTcpHealthCheck]:
        return typing.cast(typing.Optional[ComputeRegionHealthCheckTcpHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionHealthCheckTcpHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cf2067b79b9dbbd2d59bbaa043572a5d4e41ddb5f5f9cfefa2e527cace8b207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeRegionHealthCheckTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#create ComputeRegionHealthCheck#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#delete ComputeRegionHealthCheck#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#update ComputeRegionHealthCheck#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1257fa137ac40c212ec563a34d955c774c8880d04dc3f5f3f5b26cef48be015)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#create ComputeRegionHealthCheck#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#delete ComputeRegionHealthCheck#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_health_check#update ComputeRegionHealthCheck#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionHealthCheckTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionHealthCheckTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionHealthCheck.ComputeRegionHealthCheckTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ab1f2b8d2395c4a17ad365d12238d3accfe025414e932e950a33ceadae7e1cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6aec59c226aa9e7fd2139d912ffa766c9ea72d4a80046eb0aabdfc6e72745c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c584aee15d307bd83bdd59021e0117e863bec9746664e6f2197da5aeff36e245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6412e56c8d4a7fd79909ba925d25149aa44f01ad37f44814f5f04b3d42e548a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionHealthCheckTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionHealthCheckTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionHealthCheckTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25edbb55f25e209c4f2117b237b5b44558feb93ca23f8ad5d46db57755e566a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRegionHealthCheck",
    "ComputeRegionHealthCheckConfig",
    "ComputeRegionHealthCheckGrpcHealthCheck",
    "ComputeRegionHealthCheckGrpcHealthCheckOutputReference",
    "ComputeRegionHealthCheckHttp2HealthCheck",
    "ComputeRegionHealthCheckHttp2HealthCheckOutputReference",
    "ComputeRegionHealthCheckHttpHealthCheck",
    "ComputeRegionHealthCheckHttpHealthCheckOutputReference",
    "ComputeRegionHealthCheckHttpsHealthCheck",
    "ComputeRegionHealthCheckHttpsHealthCheckOutputReference",
    "ComputeRegionHealthCheckLogConfig",
    "ComputeRegionHealthCheckLogConfigOutputReference",
    "ComputeRegionHealthCheckSslHealthCheck",
    "ComputeRegionHealthCheckSslHealthCheckOutputReference",
    "ComputeRegionHealthCheckTcpHealthCheck",
    "ComputeRegionHealthCheckTcpHealthCheckOutputReference",
    "ComputeRegionHealthCheckTimeouts",
    "ComputeRegionHealthCheckTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a17996944d215ea73d175d44dc4c0b0a01794a871223e69a62a12d470b8a8695(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    check_interval_sec: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    grpc_health_check: typing.Optional[typing.Union[ComputeRegionHealthCheckGrpcHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    healthy_threshold: typing.Optional[jsii.Number] = None,
    http2_health_check: typing.Optional[typing.Union[ComputeRegionHealthCheckHttp2HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    http_health_check: typing.Optional[typing.Union[ComputeRegionHealthCheckHttpHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    https_health_check: typing.Optional[typing.Union[ComputeRegionHealthCheckHttpsHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[ComputeRegionHealthCheckLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    ssl_health_check: typing.Optional[typing.Union[ComputeRegionHealthCheckSslHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    tcp_health_check: typing.Optional[typing.Union[ComputeRegionHealthCheckTcpHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionHealthCheckTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0a2813e8798cf0d6d4e9af4620aff0a106b67c0490897ad6971847b367240e93(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f43706ea46a596554690b7d753d38ad5cd656046c5bf234a0660f826cb2ef6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74273865dd2abfaff6f346f5d3b0c55f2492f405a19b783bcf716a24ad75fb4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e50026daaef5bfd2eeb4559dd726f0ce1a14551ed2b4766b0da517e96370ff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de681bc2db2c5ff0538a05f5f4a94bb7d6d85b86d38bd138c590a688f14b22f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1520e2c2421c67685463bcf5eb7c71a808f3cb8ef563429c707747340159e1a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa109ddf461422f453020be09ded075667419c202be277fc6074ce99582b8284(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a35ede31ceb484a5832d93168f02eb4dfde246ed79edb0f86b177d89ffa4f20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc59790d798377ea7bd566f5d6bd59129c8b7cb41000197edde3eed11a35d8a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb1b31cf9e052798bde1a398e0dcb5cad79d210a65ffdbd56fffc3f5c9359aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb251f0cde36d33e9e03f48f1a3b0d90679bfe39f92fd72d5f33f957e87fdaa(
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
    grpc_health_check: typing.Optional[typing.Union[ComputeRegionHealthCheckGrpcHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    healthy_threshold: typing.Optional[jsii.Number] = None,
    http2_health_check: typing.Optional[typing.Union[ComputeRegionHealthCheckHttp2HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    http_health_check: typing.Optional[typing.Union[ComputeRegionHealthCheckHttpHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    https_health_check: typing.Optional[typing.Union[ComputeRegionHealthCheckHttpsHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[ComputeRegionHealthCheckLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    ssl_health_check: typing.Optional[typing.Union[ComputeRegionHealthCheckSslHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    tcp_health_check: typing.Optional[typing.Union[ComputeRegionHealthCheckTcpHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionHealthCheckTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_sec: typing.Optional[jsii.Number] = None,
    unhealthy_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a82c5465465f3aa672866eea82dcad697d6b42d6288ab0cba0b79a700a18d4(
    *,
    grpc_service_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    port_name: typing.Optional[builtins.str] = None,
    port_specification: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04e949b149ddf11b83b8a64dae7f559f1c40954db400f4f9eeb7f9123706850(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36cd381e55f3dfa091d22ebd1d7f7e66e8fc98bc7a2431f6ea814a5a19760c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c26420a09ef5849142989ec09e896861744599c0050c998c6bb3a09fc8fcbed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351066719bbb2f4ef1d125786c3f85a602dcf31447d5d06dd427b60f26751a78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c6ecec21449e4c4443ccdfa8608e04b45f6b3636a58f92936885862199e5b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716d3b0b156400f0d5b08ea0be0e4a205a4c27aaf84a92e6f0e7f7f319e66660(
    value: typing.Optional[ComputeRegionHealthCheckGrpcHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e59258114bd2afab208627e881548142e81e919c65eb45a069542d44a84001(
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

def _typecheckingstub__3a397806b906aeabbb8b82e426a72a2487ec522e15a1212a40d6fa6a853ddb0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4125ad9c9ed151be62cf9867856052aa6523917217eec1eb310cbd72ea8c4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd1a5c06eca2afbb5fa1dd827845836d1c532df1fd3e49088231f36f9fc4c78(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b50e84f8445fe93522f8ae157f2af1c12e83edb4b3428ca3a3256d0d301dd06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca36202b388fbc2932f1c5b7c1178a65c514b37373a0a299934342bc96afae3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a868e44d0cb80deb40567099cb9019b7b471568680ba7b4f7b98be80303f8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8795ac1908c9f1ec316d5cdbf6c75cfc7cccced6da489798ffe4fe364c7c2b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b331d80bec721095206957d5f1b09ce622c8e5c6c699f5d67590e02ceeae64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb165b6cc82a2c95ecbc5e90abc463b09e762830fb02b9ac5379725327c9e74(
    value: typing.Optional[ComputeRegionHealthCheckHttp2HealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91a6d0942d41046a007309780b463a91add8c8bb15ea4e4491b51bbf80d8b8b(
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

def _typecheckingstub__93eeae04aa25cfbc6e370a9afc66876ea169cde5b9bc9453f9a963d433a4d5e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d3e87d81522f5771a6ea54a371871ae81bdb3a7f3df074322b581ed1de114e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0615e1df2d43d02d3e0a859933e904472ae73d735cea8ebdc3f2419bbed6c22d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7033f4ef990af71f55ce18f358a47816344c0169b48cc389c0d99734701a5056(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5603a7b72bc5a71729f1b5b2468d356d37ac26575278f50075b52bd9797f4cef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21914ee92e53241822f9f1f8856374d3bb050fd3629da1974edbe115a373b85e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0887dd50ca938129cca0655910a828e70221329c6f2e2035185aa4fe56cca6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2156a76e2202739bd7a891b0aa6a68f0479efbe808ae848e00f5f9f05c2959f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d13e6c3cab6ce35625de785f6fddd9afc2af91d40315aab1691d68cd536c543(
    value: typing.Optional[ComputeRegionHealthCheckHttpHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7067a0396f45a928a5e1157a1fd2a9f7e368ad1a71d6c90ca7a8ca5e6e5805b(
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

def _typecheckingstub__bbdb3a491fd0f466eccb700b4d374c970c4203869e4a0879d65d4936d0976d4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e98cda82ab79572404f6e9bbf8718702b9c7bd57743e3a64be381e6d2698a44e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9022dbae48bcf42b5db002f86bb902d9fc1cc82b558859bdec6feb1346cfca66(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de5cd01f05a3d2e50f68bc10a8aea92378cde96de1561bc6d22e61bbf3dcb5d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c54483615c013d1913314cc9b44c07f800686bb42e6e55836afc29cf4b51cb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05875cb1f9002420e5d84232d8749bc137ed998773a6784085d1cc5837345daf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced151ace3c15628b1a64962faaf1b1a1870c6c4a2c92d8a5ace067308e3ff78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4014488d8281e3d971b28ecd1d3e65d9ec1605cecd3c289a6ae7f57bb5497f6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a5b77cb287b18f12a28a1c396fa9a1617ebd790041276b0aadd41781589002(
    value: typing.Optional[ComputeRegionHealthCheckHttpsHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468654a1ab5bdc05b9256402cc0b77c68c406cda30340d6d74f87ee9e6ae6e4e(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4de01ba316e1a8c7e9f5159625829e8c95804d063e7a283b2cc7bb0155eed43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e2b8edd5f569338b6889e34efda9bf7acbc83f7fc37cb1672a23e0593760ce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c816cb983bd47a5600f9df6d99ed2c1fdd66e62285e26788e5e597060e103cf3(
    value: typing.Optional[ComputeRegionHealthCheckLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64ca4875db131f37e11bc17f42a978600de6ecc87f8c1fe9768e67f763179d3(
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

def _typecheckingstub__c9576d8cc8b0e923d2d1642d0ec4fb3d68f41287033dd7a8ec08cf5e8d0cce35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37780262cd2c84b86bfffa2c0e752794eebaf672ad8c9c4f62758d093a92161b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d053945a0b5f63f4c56b8b94584152b4681d4ea4c955a43676bb288724753ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a80a74166cf28ba8f908e8ecb29bdc1460fa365aea9829a77f97ede5195947(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce69857a61277410c74097aebd41c0478066f6687db9107d72f66cb0c29d978(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74379d53d56679ba65937e2a9f1828a116e1e044800d1c0b39405e820175196(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ac5de68c22773b01dee8d9f9d0b69c53bfdcfb7a93159d4f02e5b5189aa478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e5824699d09d90669babf5dad282fde0690f5f7a5f7ea5dc0d936575dbb7fd(
    value: typing.Optional[ComputeRegionHealthCheckSslHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1b83d5f084ce34a0b0629ac8551534e956a870a3f873498042f8b168d92fe9(
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

def _typecheckingstub__92d6fbea4d8225e61040b6f3115907df5eff05468aa9fb66186e9c450980fee2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9516c89ee100318adaeb5fee887c0ee4bf1dec5ef0421ee5fcee3d70333f5c16(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a84def36f1a0fbf290fa87ef5aa83fec0594c5ccecac06f8bb610233fe4d6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7faddeac4abf57f5227e09605e9a8ad61cc9f2c5093d44c1c0d9b56428648f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c50c51b75cd659bcb14c966e6da177c8302bb313eab0e1429fe461e874d53af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5675c6ce35e01a40fd28e931c472af7fda2f9a3e5b361fb0d33dabfdc73b46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27da4ea1dbae99575447f37a38033203f16246b48ee2cd01bf5ad6d3f8fbc9af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf2067b79b9dbbd2d59bbaa043572a5d4e41ddb5f5f9cfefa2e527cace8b207(
    value: typing.Optional[ComputeRegionHealthCheckTcpHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1257fa137ac40c212ec563a34d955c774c8880d04dc3f5f3f5b26cef48be015(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab1f2b8d2395c4a17ad365d12238d3accfe025414e932e950a33ceadae7e1cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6aec59c226aa9e7fd2139d912ffa766c9ea72d4a80046eb0aabdfc6e72745c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c584aee15d307bd83bdd59021e0117e863bec9746664e6f2197da5aeff36e245(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6412e56c8d4a7fd79909ba925d25149aa44f01ad37f44814f5f04b3d42e548a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25edbb55f25e209c4f2117b237b5b44558feb93ca23f8ad5d46db57755e566a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionHealthCheckTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
