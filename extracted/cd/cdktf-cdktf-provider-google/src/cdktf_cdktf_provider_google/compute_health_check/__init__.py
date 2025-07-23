r'''
# `google_compute_health_check`

Refer to the Terraform Registry for docs: [`google_compute_health_check`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check).
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


class ComputeHealthCheck(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheck",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check google_compute_health_check}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        check_interval_sec: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        grpc_health_check: typing.Optional[typing.Union["ComputeHealthCheckGrpcHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        healthy_threshold: typing.Optional[jsii.Number] = None,
        http2_health_check: typing.Optional[typing.Union["ComputeHealthCheckHttp2HealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        http_health_check: typing.Optional[typing.Union["ComputeHealthCheckHttpHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        https_health_check: typing.Optional[typing.Union["ComputeHealthCheckHttpsHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["ComputeHealthCheckLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        source_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssl_health_check: typing.Optional[typing.Union["ComputeHealthCheckSslHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        tcp_health_check: typing.Optional[typing.Union["ComputeHealthCheckTcpHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeHealthCheckTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check google_compute_health_check} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#name ComputeHealthCheck#name}
        :param check_interval_sec: How often (in seconds) to send a health check. The default value is 5 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#check_interval_sec ComputeHealthCheck#check_interval_sec}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#description ComputeHealthCheck#description}
        :param grpc_health_check: grpc_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#grpc_health_check ComputeHealthCheck#grpc_health_check}
        :param healthy_threshold: A so-far unhealthy instance will be marked healthy after this many consecutive successes. The default value is 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#healthy_threshold ComputeHealthCheck#healthy_threshold}
        :param http2_health_check: http2_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#http2_health_check ComputeHealthCheck#http2_health_check}
        :param http_health_check: http_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#http_health_check ComputeHealthCheck#http_health_check}
        :param https_health_check: https_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#https_health_check ComputeHealthCheck#https_health_check}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#id ComputeHealthCheck#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#log_config ComputeHealthCheck#log_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#project ComputeHealthCheck#project}.
        :param source_regions: The list of cloud regions from which health checks are performed. If any regions are specified, then exactly 3 regions should be specified. The region names must be valid names of Google Cloud regions. This can only be set for global health check. If this list is non-empty, then there are restrictions on what other health check fields are supported and what other resources can use this health check: - SSL, HTTP2, and GRPC protocols are not supported. - The TCP request field is not supported. - The proxyHeader field for HTTP, HTTPS, and TCP is not supported. - The checkIntervalSec field must be at least 30. - The health check cannot be used with BackendService nor with managed instance group auto-healing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#source_regions ComputeHealthCheck#source_regions}
        :param ssl_health_check: ssl_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#ssl_health_check ComputeHealthCheck#ssl_health_check}
        :param tcp_health_check: tcp_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#tcp_health_check ComputeHealthCheck#tcp_health_check}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#timeouts ComputeHealthCheck#timeouts}
        :param timeout_sec: How long (in seconds) to wait before claiming failure. The default value is 5 seconds. It is invalid for timeoutSec to have greater value than checkIntervalSec. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#timeout_sec ComputeHealthCheck#timeout_sec}
        :param unhealthy_threshold: A so-far healthy instance will be marked unhealthy after this many consecutive failures. The default value is 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#unhealthy_threshold ComputeHealthCheck#unhealthy_threshold}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415ec2b591616603f55f4a01b5fa0b57b8f3e3abe8828fcda550df4daf95684f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeHealthCheckConfig(
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
            source_regions=source_regions,
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
        '''Generates CDKTF code for importing a ComputeHealthCheck resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeHealthCheck to import.
        :param import_from_id: The id of the existing ComputeHealthCheck that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeHealthCheck to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448b92081d6b6d1c957d927591bb236e655e14f19112253497fc3e2f7f15cee3)
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
        :param grpc_service_name: The gRPC service name for the health check. The value of grpcServiceName has the following meanings by convention: - Empty serviceName means the overall status of all services at the backend. - Non-empty serviceName means the health of that gRPC service, as defined by the owner of the service. The grpcServiceName can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#grpc_service_name ComputeHealthCheck#grpc_service_name}
        :param port: The port number for the health check request. Must be specified if portName and portSpecification are not set or if port_specification is USE_FIXED_PORT. Valid values are 1 through 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, gRPC health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        '''
        value = ComputeHealthCheckGrpcHealthCheck(
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
        :param host: The value of the host header in the HTTP2 health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#host ComputeHealthCheck#host}
        :param port: The TCP port number for the HTTP2 health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTP2 health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#proxy_header ComputeHealthCheck#proxy_header}
        :param request_path: The request path of the HTTP2 health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#request_path ComputeHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#response ComputeHealthCheck#response}
        '''
        value = ComputeHealthCheckHttp2HealthCheck(
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
        :param host: The value of the host header in the HTTP health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#host ComputeHealthCheck#host}
        :param port: The TCP port number for the HTTP health check request. The default value is 80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTP health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#proxy_header ComputeHealthCheck#proxy_header}
        :param request_path: The request path of the HTTP health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#request_path ComputeHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#response ComputeHealthCheck#response}
        '''
        value = ComputeHealthCheckHttpHealthCheck(
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
        :param host: The value of the host header in the HTTPS health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#host ComputeHealthCheck#host}
        :param port: The TCP port number for the HTTPS health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTPS health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#proxy_header ComputeHealthCheck#proxy_header}
        :param request_path: The request path of the HTTPS health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#request_path ComputeHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#response ComputeHealthCheck#response}
        '''
        value = ComputeHealthCheckHttpsHealthCheck(
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
        :param enable: Indicates whether or not to export logs. This is false by default, which means no health check logging will be done. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#enable ComputeHealthCheck#enable}
        '''
        value = ComputeHealthCheckLogConfig(enable=enable)

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
        :param port: The TCP port number for the SSL health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, SSL health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#proxy_header ComputeHealthCheck#proxy_header}
        :param request: The application data to send once the SSL connection has been established (default value is empty). If both request and response are empty, the connection establishment alone will indicate health. The request data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#request ComputeHealthCheck#request}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#response ComputeHealthCheck#response}
        '''
        value = ComputeHealthCheckSslHealthCheck(
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
        :param port: The TCP port number for the TCP health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, TCP health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#proxy_header ComputeHealthCheck#proxy_header}
        :param request: The application data to send once the TCP connection has been established (default value is empty). If both request and response are empty, the connection establishment alone will indicate health. The request data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#request ComputeHealthCheck#request}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#response ComputeHealthCheck#response}
        '''
        value = ComputeHealthCheckTcpHealthCheck(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#create ComputeHealthCheck#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#delete ComputeHealthCheck#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#update ComputeHealthCheck#update}.
        '''
        value = ComputeHealthCheckTimeouts(create=create, delete=delete, update=update)

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

    @jsii.member(jsii_name="resetSourceRegions")
    def reset_source_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceRegions", []))

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
    def grpc_health_check(self) -> "ComputeHealthCheckGrpcHealthCheckOutputReference":
        return typing.cast("ComputeHealthCheckGrpcHealthCheckOutputReference", jsii.get(self, "grpcHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="http2HealthCheck")
    def http2_health_check(self) -> "ComputeHealthCheckHttp2HealthCheckOutputReference":
        return typing.cast("ComputeHealthCheckHttp2HealthCheckOutputReference", jsii.get(self, "http2HealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="httpHealthCheck")
    def http_health_check(self) -> "ComputeHealthCheckHttpHealthCheckOutputReference":
        return typing.cast("ComputeHealthCheckHttpHealthCheckOutputReference", jsii.get(self, "httpHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="httpsHealthCheck")
    def https_health_check(self) -> "ComputeHealthCheckHttpsHealthCheckOutputReference":
        return typing.cast("ComputeHealthCheckHttpsHealthCheckOutputReference", jsii.get(self, "httpsHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="logConfig")
    def log_config(self) -> "ComputeHealthCheckLogConfigOutputReference":
        return typing.cast("ComputeHealthCheckLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="sslHealthCheck")
    def ssl_health_check(self) -> "ComputeHealthCheckSslHealthCheckOutputReference":
        return typing.cast("ComputeHealthCheckSslHealthCheckOutputReference", jsii.get(self, "sslHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="tcpHealthCheck")
    def tcp_health_check(self) -> "ComputeHealthCheckTcpHealthCheckOutputReference":
        return typing.cast("ComputeHealthCheckTcpHealthCheckOutputReference", jsii.get(self, "tcpHealthCheck"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeHealthCheckTimeoutsOutputReference":
        return typing.cast("ComputeHealthCheckTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["ComputeHealthCheckGrpcHealthCheck"]:
        return typing.cast(typing.Optional["ComputeHealthCheckGrpcHealthCheck"], jsii.get(self, "grpcHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="healthyThresholdInput")
    def healthy_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthyThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="http2HealthCheckInput")
    def http2_health_check_input(
        self,
    ) -> typing.Optional["ComputeHealthCheckHttp2HealthCheck"]:
        return typing.cast(typing.Optional["ComputeHealthCheckHttp2HealthCheck"], jsii.get(self, "http2HealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHealthCheckInput")
    def http_health_check_input(
        self,
    ) -> typing.Optional["ComputeHealthCheckHttpHealthCheck"]:
        return typing.cast(typing.Optional["ComputeHealthCheckHttpHealthCheck"], jsii.get(self, "httpHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsHealthCheckInput")
    def https_health_check_input(
        self,
    ) -> typing.Optional["ComputeHealthCheckHttpsHealthCheck"]:
        return typing.cast(typing.Optional["ComputeHealthCheckHttpsHealthCheck"], jsii.get(self, "httpsHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigInput")
    def log_config_input(self) -> typing.Optional["ComputeHealthCheckLogConfig"]:
        return typing.cast(typing.Optional["ComputeHealthCheckLogConfig"], jsii.get(self, "logConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceRegionsInput")
    def source_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sslHealthCheckInput")
    def ssl_health_check_input(
        self,
    ) -> typing.Optional["ComputeHealthCheckSslHealthCheck"]:
        return typing.cast(typing.Optional["ComputeHealthCheckSslHealthCheck"], jsii.get(self, "sslHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpHealthCheckInput")
    def tcp_health_check_input(
        self,
    ) -> typing.Optional["ComputeHealthCheckTcpHealthCheck"]:
        return typing.cast(typing.Optional["ComputeHealthCheckTcpHealthCheck"], jsii.get(self, "tcpHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecInput")
    def timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeHealthCheckTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeHealthCheckTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__735e8d1a56d729ed40a779b150620918b732e0e95ae871f946cd74c23271c527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkIntervalSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf9b296f45b27ab39fad56f2c54e2acec5c28c19e15bcdf0aaca8179cecea09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthyThreshold")
    def healthy_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthyThreshold"))

    @healthy_threshold.setter
    def healthy_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8d29ac246791443e3957e1b765b51aa4a3fe738e2c597412ee8298fcd0cb7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthyThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__033805f0536879f377c33f86c5abc84bdc38a3397df3283d558315f60140d084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9abaebd39b3739da07e8f107ac931efb198cde5fc675a01b764c7da7a6ffacba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df13531662b5b7e05cebca7329d4068af4cce1e9efb58800f45afba4aac4b3b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceRegions")
    def source_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceRegions"))

    @source_regions.setter
    def source_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62e8917b7be96c40fe3188b5e0f4e00edb8a1f89660c6d890a94ba350e86af97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSec")
    def timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSec"))

    @timeout_sec.setter
    def timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eb08bf4039cfa41cffcacc6ea493caf374280f35d17e6d36ee5a037a8bd1f77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unhealthyThreshold")
    def unhealthy_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unhealthyThreshold"))

    @unhealthy_threshold.setter
    def unhealthy_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1509c4bad9773d6b284359301719397bab941a59bce70580f46e15cb97a22a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unhealthyThreshold", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckConfig",
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
        "source_regions": "sourceRegions",
        "ssl_health_check": "sslHealthCheck",
        "tcp_health_check": "tcpHealthCheck",
        "timeouts": "timeouts",
        "timeout_sec": "timeoutSec",
        "unhealthy_threshold": "unhealthyThreshold",
    },
)
class ComputeHealthCheckConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        grpc_health_check: typing.Optional[typing.Union["ComputeHealthCheckGrpcHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        healthy_threshold: typing.Optional[jsii.Number] = None,
        http2_health_check: typing.Optional[typing.Union["ComputeHealthCheckHttp2HealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        http_health_check: typing.Optional[typing.Union["ComputeHealthCheckHttpHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        https_health_check: typing.Optional[typing.Union["ComputeHealthCheckHttpsHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["ComputeHealthCheckLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        source_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssl_health_check: typing.Optional[typing.Union["ComputeHealthCheckSslHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        tcp_health_check: typing.Optional[typing.Union["ComputeHealthCheckTcpHealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeHealthCheckTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#name ComputeHealthCheck#name}
        :param check_interval_sec: How often (in seconds) to send a health check. The default value is 5 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#check_interval_sec ComputeHealthCheck#check_interval_sec}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#description ComputeHealthCheck#description}
        :param grpc_health_check: grpc_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#grpc_health_check ComputeHealthCheck#grpc_health_check}
        :param healthy_threshold: A so-far unhealthy instance will be marked healthy after this many consecutive successes. The default value is 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#healthy_threshold ComputeHealthCheck#healthy_threshold}
        :param http2_health_check: http2_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#http2_health_check ComputeHealthCheck#http2_health_check}
        :param http_health_check: http_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#http_health_check ComputeHealthCheck#http_health_check}
        :param https_health_check: https_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#https_health_check ComputeHealthCheck#https_health_check}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#id ComputeHealthCheck#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#log_config ComputeHealthCheck#log_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#project ComputeHealthCheck#project}.
        :param source_regions: The list of cloud regions from which health checks are performed. If any regions are specified, then exactly 3 regions should be specified. The region names must be valid names of Google Cloud regions. This can only be set for global health check. If this list is non-empty, then there are restrictions on what other health check fields are supported and what other resources can use this health check: - SSL, HTTP2, and GRPC protocols are not supported. - The TCP request field is not supported. - The proxyHeader field for HTTP, HTTPS, and TCP is not supported. - The checkIntervalSec field must be at least 30. - The health check cannot be used with BackendService nor with managed instance group auto-healing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#source_regions ComputeHealthCheck#source_regions}
        :param ssl_health_check: ssl_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#ssl_health_check ComputeHealthCheck#ssl_health_check}
        :param tcp_health_check: tcp_health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#tcp_health_check ComputeHealthCheck#tcp_health_check}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#timeouts ComputeHealthCheck#timeouts}
        :param timeout_sec: How long (in seconds) to wait before claiming failure. The default value is 5 seconds. It is invalid for timeoutSec to have greater value than checkIntervalSec. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#timeout_sec ComputeHealthCheck#timeout_sec}
        :param unhealthy_threshold: A so-far healthy instance will be marked unhealthy after this many consecutive failures. The default value is 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#unhealthy_threshold ComputeHealthCheck#unhealthy_threshold}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(grpc_health_check, dict):
            grpc_health_check = ComputeHealthCheckGrpcHealthCheck(**grpc_health_check)
        if isinstance(http2_health_check, dict):
            http2_health_check = ComputeHealthCheckHttp2HealthCheck(**http2_health_check)
        if isinstance(http_health_check, dict):
            http_health_check = ComputeHealthCheckHttpHealthCheck(**http_health_check)
        if isinstance(https_health_check, dict):
            https_health_check = ComputeHealthCheckHttpsHealthCheck(**https_health_check)
        if isinstance(log_config, dict):
            log_config = ComputeHealthCheckLogConfig(**log_config)
        if isinstance(ssl_health_check, dict):
            ssl_health_check = ComputeHealthCheckSslHealthCheck(**ssl_health_check)
        if isinstance(tcp_health_check, dict):
            tcp_health_check = ComputeHealthCheckTcpHealthCheck(**tcp_health_check)
        if isinstance(timeouts, dict):
            timeouts = ComputeHealthCheckTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f05c586585bf1aeea6123ed7babbf2b25edc1fe5c15cb99f0e3486756eb40b9)
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
            check_type(argname="argument source_regions", value=source_regions, expected_type=type_hints["source_regions"])
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
        if source_regions is not None:
            self._values["source_regions"] = source_regions
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#name ComputeHealthCheck#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def check_interval_sec(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to send a health check. The default value is 5 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#check_interval_sec ComputeHealthCheck#check_interval_sec}
        '''
        result = self._values.get("check_interval_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#description ComputeHealthCheck#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grpc_health_check(self) -> typing.Optional["ComputeHealthCheckGrpcHealthCheck"]:
        '''grpc_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#grpc_health_check ComputeHealthCheck#grpc_health_check}
        '''
        result = self._values.get("grpc_health_check")
        return typing.cast(typing.Optional["ComputeHealthCheckGrpcHealthCheck"], result)

    @builtins.property
    def healthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''A so-far unhealthy instance will be marked healthy after this many consecutive successes. The default value is 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#healthy_threshold ComputeHealthCheck#healthy_threshold}
        '''
        result = self._values.get("healthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def http2_health_check(
        self,
    ) -> typing.Optional["ComputeHealthCheckHttp2HealthCheck"]:
        '''http2_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#http2_health_check ComputeHealthCheck#http2_health_check}
        '''
        result = self._values.get("http2_health_check")
        return typing.cast(typing.Optional["ComputeHealthCheckHttp2HealthCheck"], result)

    @builtins.property
    def http_health_check(self) -> typing.Optional["ComputeHealthCheckHttpHealthCheck"]:
        '''http_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#http_health_check ComputeHealthCheck#http_health_check}
        '''
        result = self._values.get("http_health_check")
        return typing.cast(typing.Optional["ComputeHealthCheckHttpHealthCheck"], result)

    @builtins.property
    def https_health_check(
        self,
    ) -> typing.Optional["ComputeHealthCheckHttpsHealthCheck"]:
        '''https_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#https_health_check ComputeHealthCheck#https_health_check}
        '''
        result = self._values.get("https_health_check")
        return typing.cast(typing.Optional["ComputeHealthCheckHttpsHealthCheck"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#id ComputeHealthCheck#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_config(self) -> typing.Optional["ComputeHealthCheckLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#log_config ComputeHealthCheck#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["ComputeHealthCheckLogConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#project ComputeHealthCheck#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of cloud regions from which health checks are performed.

        If
        any regions are specified, then exactly 3 regions should be specified.
        The region names must be valid names of Google Cloud regions. This can
        only be set for global health check. If this list is non-empty, then
        there are restrictions on what other health check fields are supported
        and what other resources can use this health check:

        - SSL, HTTP2, and GRPC protocols are not supported.
        - The TCP request field is not supported.
        - The proxyHeader field for HTTP, HTTPS, and TCP is not supported.
        - The checkIntervalSec field must be at least 30.
        - The health check cannot be used with BackendService nor with managed
          instance group auto-healing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#source_regions ComputeHealthCheck#source_regions}
        '''
        result = self._values.get("source_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ssl_health_check(self) -> typing.Optional["ComputeHealthCheckSslHealthCheck"]:
        '''ssl_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#ssl_health_check ComputeHealthCheck#ssl_health_check}
        '''
        result = self._values.get("ssl_health_check")
        return typing.cast(typing.Optional["ComputeHealthCheckSslHealthCheck"], result)

    @builtins.property
    def tcp_health_check(self) -> typing.Optional["ComputeHealthCheckTcpHealthCheck"]:
        '''tcp_health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#tcp_health_check ComputeHealthCheck#tcp_health_check}
        '''
        result = self._values.get("tcp_health_check")
        return typing.cast(typing.Optional["ComputeHealthCheckTcpHealthCheck"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeHealthCheckTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#timeouts ComputeHealthCheck#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeHealthCheckTimeouts"], result)

    @builtins.property
    def timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''How long (in seconds) to wait before claiming failure.

        The default value is 5 seconds.  It is invalid for timeoutSec to have
        greater value than checkIntervalSec.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#timeout_sec ComputeHealthCheck#timeout_sec}
        '''
        result = self._values.get("timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''A so-far healthy instance will be marked unhealthy after this many consecutive failures. The default value is 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#unhealthy_threshold ComputeHealthCheck#unhealthy_threshold}
        '''
        result = self._values.get("unhealthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeHealthCheckConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckGrpcHealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "grpc_service_name": "grpcServiceName",
        "port": "port",
        "port_name": "portName",
        "port_specification": "portSpecification",
    },
)
class ComputeHealthCheckGrpcHealthCheck:
    def __init__(
        self,
        *,
        grpc_service_name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        port_name: typing.Optional[builtins.str] = None,
        port_specification: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param grpc_service_name: The gRPC service name for the health check. The value of grpcServiceName has the following meanings by convention: - Empty serviceName means the overall status of all services at the backend. - Non-empty serviceName means the health of that gRPC service, as defined by the owner of the service. The grpcServiceName can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#grpc_service_name ComputeHealthCheck#grpc_service_name}
        :param port: The port number for the health check request. Must be specified if portName and portSpecification are not set or if port_specification is USE_FIXED_PORT. Valid values are 1 through 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, gRPC health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350bd09e2658e569437a78f00e384b0efa4cf313a9ca61b8b4d548461efce824)
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
        '''The gRPC service name for the health check.

        The value of grpcServiceName has the following meanings by convention:

        - Empty serviceName means the overall status of all services at the backend.
        - Non-empty serviceName means the health of that gRPC service, as defined by the owner of the service.
          The grpcServiceName can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#grpc_service_name ComputeHealthCheck#grpc_service_name}
        '''
        result = self._values.get("grpc_service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port number for the health check request.

        Must be specified if portName and portSpecification are not set
        or if port_specification is USE_FIXED_PORT. Valid values are 1 through 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeHealthCheckGrpcHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeHealthCheckGrpcHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckGrpcHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb5bc26388512c7a9f1703bd2b2ce3567fb9e378d1ab0b5c5f088f4ac02d1870)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5af92930ae2ea9be4c04855b51629f958a4911a6d109586bb966d06a95a2ae7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grpcServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1df33775896c950741d4319af0b19b44ddfb4cb50a92dbcce4e98217fb88ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68224a7c6dc0f4d8bd5516eae54adf249a6ea31878482ccd395123f2c850b83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01ecc0dbc0912b4ca9f7e6c729adfe209af15e841a0ef3ba88d0bb0638a9329d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeHealthCheckGrpcHealthCheck]:
        return typing.cast(typing.Optional[ComputeHealthCheckGrpcHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeHealthCheckGrpcHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c3d45ed99eb4dc983200cb3d8074b0686ad4a81c9630308957eaf46c100fba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckHttp2HealthCheck",
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
class ComputeHealthCheckHttp2HealthCheck:
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
        :param host: The value of the host header in the HTTP2 health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#host ComputeHealthCheck#host}
        :param port: The TCP port number for the HTTP2 health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTP2 health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#proxy_header ComputeHealthCheck#proxy_header}
        :param request_path: The request path of the HTTP2 health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#request_path ComputeHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#response ComputeHealthCheck#response}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d404e71087a3550ff1eee4601500271712e31fc7e687bd82fa4f4766066f2b31)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#host ComputeHealthCheck#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The TCP port number for the HTTP2 health check request. The default value is 443.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_header(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of proxy header to append before sending data to the backend.

        Default value: "NONE" Possible values: ["NONE", "PROXY_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#proxy_header ComputeHealthCheck#proxy_header}
        '''
        result = self._values.get("proxy_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_path(self) -> typing.Optional[builtins.str]:
        '''The request path of the HTTP2 health check request. The default value is /.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#request_path ComputeHealthCheck#request_path}
        '''
        result = self._values.get("request_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''The bytes to match against the beginning of the response data.

        If left empty
        (the default value), any response will indicate health. The response data
        can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#response ComputeHealthCheck#response}
        '''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeHealthCheckHttp2HealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeHealthCheckHttp2HealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckHttp2HealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83ecaa45b9b2ea1a9f5c1268b1918ca3c85bcd539c414446fd5aac28a006a4f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4121bf41cddc20e7f5cc3bfc03bceae10ffdec2fcab6de8e2ca412c16762130b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35a1dc6c21c21871855a808be1a30021e6eecfc902978a855c993a9b5f1b108d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f0664a3c54b871b6e9c6a422841f54df406028eeaefdf3bffb5da5ae84b427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5e3b360046ed324587fc853ef009282c6d05bbd652ceed36b6b0ce36513b13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyHeader")
    def proxy_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyHeader"))

    @proxy_header.setter
    def proxy_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f72f9f924e832923c21e80d63b778f3aa92d5f7398eeec56d857f4a2344530)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestPath")
    def request_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestPath"))

    @request_path.setter
    def request_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7afd94dc97bca0b46d1860d75583a30e405b03fc6cfb9ec72ed02db2b9eb5d46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__178ddcf6d2c4d287c8945101387422f11d7b39d179e31dfa2bd74021f53fa79f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeHealthCheckHttp2HealthCheck]:
        return typing.cast(typing.Optional[ComputeHealthCheckHttp2HealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeHealthCheckHttp2HealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad8abbfb365cb5d93a94d20ca1115c699bf1560e670684c323f5ef747036231f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckHttpHealthCheck",
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
class ComputeHealthCheckHttpHealthCheck:
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
        :param host: The value of the host header in the HTTP health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#host ComputeHealthCheck#host}
        :param port: The TCP port number for the HTTP health check request. The default value is 80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTP health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#proxy_header ComputeHealthCheck#proxy_header}
        :param request_path: The request path of the HTTP health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#request_path ComputeHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#response ComputeHealthCheck#response}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d36014ec787656e8a314104f9f6ee59a9bb890d5813673b0da1abcc7b875bcc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#host ComputeHealthCheck#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The TCP port number for the HTTP health check request. The default value is 80.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_header(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of proxy header to append before sending data to the backend.

        Default value: "NONE" Possible values: ["NONE", "PROXY_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#proxy_header ComputeHealthCheck#proxy_header}
        '''
        result = self._values.get("proxy_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_path(self) -> typing.Optional[builtins.str]:
        '''The request path of the HTTP health check request. The default value is /.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#request_path ComputeHealthCheck#request_path}
        '''
        result = self._values.get("request_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''The bytes to match against the beginning of the response data.

        If left empty
        (the default value), any response will indicate health. The response data
        can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#response ComputeHealthCheck#response}
        '''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeHealthCheckHttpHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeHealthCheckHttpHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckHttpHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da37af59c115ee59a702da684e6167cf7767a06e260d4ebdfc94958cf5e64963)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c57511149f8d8cd3746a1e10c0d1f8d9654e76f6168c33d1bd1cdae399fd75a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95b396f6229f077548e3437de7728974408137bbaca98b0be39bf180cc0b37d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad2ba0d0c75f30f0d08695e4f90c90fdc808b5fc97f1d7d623e31f652b930861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1884fbaa275163dd8578e1d1f489d811e2bbc3bdb045811a2bb60677ec728a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyHeader")
    def proxy_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyHeader"))

    @proxy_header.setter
    def proxy_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e17860fc8ffeab92467ee9774e1a778804b9a444f6d2e8fb89ed197f5b8299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestPath")
    def request_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestPath"))

    @request_path.setter
    def request_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81cd2bf9ce39e95cf2e157f89b548b46188b522e5e945c54663937820c77ba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__477a58d75bbe0825289f7f9fe107b3a5a7baac84bd0298d06bf3a5cfbf1879e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeHealthCheckHttpHealthCheck]:
        return typing.cast(typing.Optional[ComputeHealthCheckHttpHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeHealthCheckHttpHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8438d3641b4d73721e7684e6154e31df81d144bb8e0ab8744f04280f8e48246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckHttpsHealthCheck",
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
class ComputeHealthCheckHttpsHealthCheck:
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
        :param host: The value of the host header in the HTTPS health check request. If left empty (default value), the public IP on behalf of which this health check is performed will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#host ComputeHealthCheck#host}
        :param port: The TCP port number for the HTTPS health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, HTTPS health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#proxy_header ComputeHealthCheck#proxy_header}
        :param request_path: The request path of the HTTPS health check request. The default value is /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#request_path ComputeHealthCheck#request_path}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#response ComputeHealthCheck#response}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f6ffbfdc5a67a90c3374511699a0120b1cfd649653ced1ba24bf80825b61c8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#host ComputeHealthCheck#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The TCP port number for the HTTPS health check request. The default value is 443.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_header(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of proxy header to append before sending data to the backend.

        Default value: "NONE" Possible values: ["NONE", "PROXY_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#proxy_header ComputeHealthCheck#proxy_header}
        '''
        result = self._values.get("proxy_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_path(self) -> typing.Optional[builtins.str]:
        '''The request path of the HTTPS health check request. The default value is /.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#request_path ComputeHealthCheck#request_path}
        '''
        result = self._values.get("request_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''The bytes to match against the beginning of the response data.

        If left empty
        (the default value), any response will indicate health. The response data
        can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#response ComputeHealthCheck#response}
        '''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeHealthCheckHttpsHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeHealthCheckHttpsHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckHttpsHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40c459fd98e9e7a8e8d187903da76f93c780d62f0981bd1442ead16fb2a7dd9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b54100a9b0e2150a957ce7c0ae12d1964a1a14d36f7e94368d329c78d456d87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc3aa27beb1823ddbf8f4d39d0727d3f8058466d28d146195dd4eca2a4b309b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15097cf586b53ea646e24abe8056433f5cf5d0fcada48b1c4b762991ae930bf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57a5e854da3592d9256aca4b4971668b12c5cb69cc2e3b373d3310b83bc7e96f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyHeader")
    def proxy_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyHeader"))

    @proxy_header.setter
    def proxy_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6621b33319a96bcae3a35af5aad003c1133a5db4137a3ec8433e2547b4d9daba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestPath")
    def request_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestPath"))

    @request_path.setter
    def request_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f6caa6e30a9b3e0c0bd8cbabc6bf51d8334ade7a617007d259d5639e909e597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be4510b82880e31bda2ed76d1982f1e9c186c05a9d71397c750af1db632951d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeHealthCheckHttpsHealthCheck]:
        return typing.cast(typing.Optional[ComputeHealthCheckHttpsHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeHealthCheckHttpsHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1c7ae29b5e6c361cf129572ac6c43b1c6e52c50be78f82e4b63527a8021ef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckLogConfig",
    jsii_struct_bases=[],
    name_mapping={"enable": "enable"},
)
class ComputeHealthCheckLogConfig:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable: Indicates whether or not to export logs. This is false by default, which means no health check logging will be done. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#enable ComputeHealthCheck#enable}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ccdb6a273fbd00dc3ff9e62d911865f5f6f2d28b9b409105a773fe86ac6620c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#enable ComputeHealthCheck#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeHealthCheckLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeHealthCheckLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e4c7ffd6e9e25e1d2a41d324fa946dd6d93e14be7f17997ada4f10edcb5b06a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0968bb4581781b812c724ff8f572f908803cfba5e8d84f2d6c272ca1e4dec8a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeHealthCheckLogConfig]:
        return typing.cast(typing.Optional[ComputeHealthCheckLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeHealthCheckLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d285c737146e3eaa2e66d112acc7a10a9108c2a9366db6617ad69d02d7d7b874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckSslHealthCheck",
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
class ComputeHealthCheckSslHealthCheck:
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
        :param port: The TCP port number for the SSL health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, SSL health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#proxy_header ComputeHealthCheck#proxy_header}
        :param request: The application data to send once the SSL connection has been established (default value is empty). If both request and response are empty, the connection establishment alone will indicate health. The request data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#request ComputeHealthCheck#request}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#response ComputeHealthCheck#response}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a628403851d8855265b12b878d510d089f22c6f9d766e9fe14051d4cb67b5acd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_header(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of proxy header to append before sending data to the backend.

        Default value: "NONE" Possible values: ["NONE", "PROXY_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#proxy_header ComputeHealthCheck#proxy_header}
        '''
        result = self._values.get("proxy_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request(self) -> typing.Optional[builtins.str]:
        '''The application data to send once the SSL connection has been established (default value is empty).

        If both request and response are
        empty, the connection establishment alone will indicate health. The request
        data can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#request ComputeHealthCheck#request}
        '''
        result = self._values.get("request")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''The bytes to match against the beginning of the response data.

        If left empty
        (the default value), any response will indicate health. The response data
        can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#response ComputeHealthCheck#response}
        '''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeHealthCheckSslHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeHealthCheckSslHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckSslHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa19c4832402c62a702baf8fc003f01c1634bd068bb893d808e4d9f002a12450)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0852cca4463c494ede949acb238041563729d3cf3fb29ff1c4017a7bec6c242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb38c7e2b94e234af3744173a5b0042ed9b3abfef01fda2ad23156c3b733761d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c32c4c65300d62a5b03d81e3ef7295879474f78976cf8c3476f9a150f520ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyHeader")
    def proxy_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyHeader"))

    @proxy_header.setter
    def proxy_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__490bd1392ed36307f8739703e1a73e7823065b3cac4db1f2b66d6077f6de915e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="request")
    def request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "request"))

    @request.setter
    def request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d82d321912f05f86157d4910e551bd6c5586739323ae92ff687b8770b160af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "request", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5a134db3a68d7239f2843e76c3bcc026853973fe5f73c5118c3afc89afc06c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeHealthCheckSslHealthCheck]:
        return typing.cast(typing.Optional[ComputeHealthCheckSslHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeHealthCheckSslHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ade1b83b37ee7425600aba740fe1d3ce05d1ba292c8402eb48e3885cc62c6e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckTcpHealthCheck",
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
class ComputeHealthCheckTcpHealthCheck:
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
        :param port: The TCP port number for the TCP health check request. The default value is 443. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        :param port_name: Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
        :param port_specification: Specifies how port is selected for health checking, can be one of the following values:. - 'USE_FIXED_PORT': The port number in 'port' is used for health checking. - 'USE_NAMED_PORT': The 'portName' is used for health checking. - 'USE_SERVING_PORT': For NetworkEndpointGroup, the port specified for each network endpoint is used for health checking. For other backends, the port or named port specified in the Backend Service is used for health checking. If not specified, TCP health check follows behavior specified in 'port' and 'portName' fields. Possible values: ["USE_FIXED_PORT", "USE_NAMED_PORT", "USE_SERVING_PORT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        :param proxy_header: Specifies the type of proxy header to append before sending data to the backend. Default value: "NONE" Possible values: ["NONE", "PROXY_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#proxy_header ComputeHealthCheck#proxy_header}
        :param request: The application data to send once the TCP connection has been established (default value is empty). If both request and response are empty, the connection establishment alone will indicate health. The request data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#request ComputeHealthCheck#request}
        :param response: The bytes to match against the beginning of the response data. If left empty (the default value), any response will indicate health. The response data can only be ASCII. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#response ComputeHealthCheck#response}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac1cd9e8c8e9adce9a8ad3ec3cdd9eb474713730c5c9b193efa61e3a68a6d03)
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
        '''The TCP port number for the TCP health check request. The default value is 443.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port ComputeHealthCheck#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''Port name as defined in InstanceGroup#NamedPort#name. If both port and port_name are defined, port takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_name ComputeHealthCheck#port_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#port_specification ComputeHealthCheck#port_specification}
        '''
        result = self._values.get("port_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_header(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of proxy header to append before sending data to the backend.

        Default value: "NONE" Possible values: ["NONE", "PROXY_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#proxy_header ComputeHealthCheck#proxy_header}
        '''
        result = self._values.get("proxy_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request(self) -> typing.Optional[builtins.str]:
        '''The application data to send once the TCP connection has been established (default value is empty).

        If both request and response are
        empty, the connection establishment alone will indicate health. The request
        data can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#request ComputeHealthCheck#request}
        '''
        result = self._values.get("request")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response(self) -> typing.Optional[builtins.str]:
        '''The bytes to match against the beginning of the response data.

        If left empty
        (the default value), any response will indicate health. The response data
        can only be ASCII.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#response ComputeHealthCheck#response}
        '''
        result = self._values.get("response")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeHealthCheckTcpHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeHealthCheckTcpHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckTcpHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38b53d301f4a7494cb72682c9e0b49e7ff3edcccd21f3be950b5d581b34739a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa8dd28f9bebc12f1f5082c96967f87182f16ccdc738813b67b1e11786d02bda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef5cebf304476a20a557b7b59e1c16e95dbf0056054b1bda95b922ef833c977)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portSpecification")
    def port_specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portSpecification"))

    @port_specification.setter
    def port_specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ec3308c84b3d69b7336d74539829f2dd9f49c3c4192f8224270bdefad0eb4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portSpecification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyHeader")
    def proxy_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyHeader"))

    @proxy_header.setter
    def proxy_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22cc92a52f632d9583f57ad901fd6aeee8c9b895107387a8580646fb45a3145d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="request")
    def request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "request"))

    @request.setter
    def request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6013c910bb38680b5a372822188eb7163abb0d1aa008a16994ef3174b6ac0ffc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "request", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="response")
    def response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "response"))

    @response.setter
    def response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57285dee17cd98beedc29dd21bb165e98e6ae7eefc3c5717bf7dd5946f99aea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "response", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeHealthCheckTcpHealthCheck]:
        return typing.cast(typing.Optional[ComputeHealthCheckTcpHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeHealthCheckTcpHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bfcb169c5b5f96ed251079dbb0c20e826e26f4bf3bd780255216dcd86508607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeHealthCheckTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#create ComputeHealthCheck#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#delete ComputeHealthCheck#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#update ComputeHealthCheck#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89140a119dbcedc86dc5967a8a39dcc71c45e8a1efd173a9a53bc110a22deb29)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#create ComputeHealthCheck#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#delete ComputeHealthCheck#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_health_check#update ComputeHealthCheck#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeHealthCheckTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeHealthCheckTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeHealthCheck.ComputeHealthCheckTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36904e39a0ca5eb1024f473324c4aaa735ae48a8b74aa67965055759d6d138cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96fdadee25e74a621c6417002c0bd128953bb2ebc028d27e1c31052e792e9405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc9527cfe79583c1a9c9e58afafaee93fe37154bf7b367f745f4a1852437186)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd5e7a97608780e0e868498c7f2566ad361f4fd5fd327ccf75841e53428c63eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeHealthCheckTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeHealthCheckTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeHealthCheckTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d283a610fa1e50af14cf5ae0d28f0fad94a1d8efa24086df1b18b72557ef4ca6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeHealthCheck",
    "ComputeHealthCheckConfig",
    "ComputeHealthCheckGrpcHealthCheck",
    "ComputeHealthCheckGrpcHealthCheckOutputReference",
    "ComputeHealthCheckHttp2HealthCheck",
    "ComputeHealthCheckHttp2HealthCheckOutputReference",
    "ComputeHealthCheckHttpHealthCheck",
    "ComputeHealthCheckHttpHealthCheckOutputReference",
    "ComputeHealthCheckHttpsHealthCheck",
    "ComputeHealthCheckHttpsHealthCheckOutputReference",
    "ComputeHealthCheckLogConfig",
    "ComputeHealthCheckLogConfigOutputReference",
    "ComputeHealthCheckSslHealthCheck",
    "ComputeHealthCheckSslHealthCheckOutputReference",
    "ComputeHealthCheckTcpHealthCheck",
    "ComputeHealthCheckTcpHealthCheckOutputReference",
    "ComputeHealthCheckTimeouts",
    "ComputeHealthCheckTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__415ec2b591616603f55f4a01b5fa0b57b8f3e3abe8828fcda550df4daf95684f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    check_interval_sec: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    grpc_health_check: typing.Optional[typing.Union[ComputeHealthCheckGrpcHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    healthy_threshold: typing.Optional[jsii.Number] = None,
    http2_health_check: typing.Optional[typing.Union[ComputeHealthCheckHttp2HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    http_health_check: typing.Optional[typing.Union[ComputeHealthCheckHttpHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    https_health_check: typing.Optional[typing.Union[ComputeHealthCheckHttpsHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[ComputeHealthCheckLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    source_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ssl_health_check: typing.Optional[typing.Union[ComputeHealthCheckSslHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    tcp_health_check: typing.Optional[typing.Union[ComputeHealthCheckTcpHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeHealthCheckTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__448b92081d6b6d1c957d927591bb236e655e14f19112253497fc3e2f7f15cee3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735e8d1a56d729ed40a779b150620918b732e0e95ae871f946cd74c23271c527(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf9b296f45b27ab39fad56f2c54e2acec5c28c19e15bcdf0aaca8179cecea09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8d29ac246791443e3957e1b765b51aa4a3fe738e2c597412ee8298fcd0cb7d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__033805f0536879f377c33f86c5abc84bdc38a3397df3283d558315f60140d084(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9abaebd39b3739da07e8f107ac931efb198cde5fc675a01b764c7da7a6ffacba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df13531662b5b7e05cebca7329d4068af4cce1e9efb58800f45afba4aac4b3b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e8917b7be96c40fe3188b5e0f4e00edb8a1f89660c6d890a94ba350e86af97(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb08bf4039cfa41cffcacc6ea493caf374280f35d17e6d36ee5a037a8bd1f77(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1509c4bad9773d6b284359301719397bab941a59bce70580f46e15cb97a22a2a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f05c586585bf1aeea6123ed7babbf2b25edc1fe5c15cb99f0e3486756eb40b9(
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
    grpc_health_check: typing.Optional[typing.Union[ComputeHealthCheckGrpcHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    healthy_threshold: typing.Optional[jsii.Number] = None,
    http2_health_check: typing.Optional[typing.Union[ComputeHealthCheckHttp2HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    http_health_check: typing.Optional[typing.Union[ComputeHealthCheckHttpHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    https_health_check: typing.Optional[typing.Union[ComputeHealthCheckHttpsHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[ComputeHealthCheckLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    source_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ssl_health_check: typing.Optional[typing.Union[ComputeHealthCheckSslHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    tcp_health_check: typing.Optional[typing.Union[ComputeHealthCheckTcpHealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeHealthCheckTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_sec: typing.Optional[jsii.Number] = None,
    unhealthy_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350bd09e2658e569437a78f00e384b0efa4cf313a9ca61b8b4d548461efce824(
    *,
    grpc_service_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    port_name: typing.Optional[builtins.str] = None,
    port_specification: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb5bc26388512c7a9f1703bd2b2ce3567fb9e378d1ab0b5c5f088f4ac02d1870(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af92930ae2ea9be4c04855b51629f958a4911a6d109586bb966d06a95a2ae7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1df33775896c950741d4319af0b19b44ddfb4cb50a92dbcce4e98217fb88ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68224a7c6dc0f4d8bd5516eae54adf249a6ea31878482ccd395123f2c850b83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ecc0dbc0912b4ca9f7e6c729adfe209af15e841a0ef3ba88d0bb0638a9329d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c3d45ed99eb4dc983200cb3d8074b0686ad4a81c9630308957eaf46c100fba(
    value: typing.Optional[ComputeHealthCheckGrpcHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d404e71087a3550ff1eee4601500271712e31fc7e687bd82fa4f4766066f2b31(
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

def _typecheckingstub__83ecaa45b9b2ea1a9f5c1268b1918ca3c85bcd539c414446fd5aac28a006a4f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4121bf41cddc20e7f5cc3bfc03bceae10ffdec2fcab6de8e2ca412c16762130b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a1dc6c21c21871855a808be1a30021e6eecfc902978a855c993a9b5f1b108d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f0664a3c54b871b6e9c6a422841f54df406028eeaefdf3bffb5da5ae84b427(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5e3b360046ed324587fc853ef009282c6d05bbd652ceed36b6b0ce36513b13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f72f9f924e832923c21e80d63b778f3aa92d5f7398eeec56d857f4a2344530(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7afd94dc97bca0b46d1860d75583a30e405b03fc6cfb9ec72ed02db2b9eb5d46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178ddcf6d2c4d287c8945101387422f11d7b39d179e31dfa2bd74021f53fa79f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8abbfb365cb5d93a94d20ca1115c699bf1560e670684c323f5ef747036231f(
    value: typing.Optional[ComputeHealthCheckHttp2HealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d36014ec787656e8a314104f9f6ee59a9bb890d5813673b0da1abcc7b875bcc(
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

def _typecheckingstub__da37af59c115ee59a702da684e6167cf7767a06e260d4ebdfc94958cf5e64963(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57511149f8d8cd3746a1e10c0d1f8d9654e76f6168c33d1bd1cdae399fd75a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b396f6229f077548e3437de7728974408137bbaca98b0be39bf180cc0b37d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad2ba0d0c75f30f0d08695e4f90c90fdc808b5fc97f1d7d623e31f652b930861(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1884fbaa275163dd8578e1d1f489d811e2bbc3bdb045811a2bb60677ec728a22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e17860fc8ffeab92467ee9774e1a778804b9a444f6d2e8fb89ed197f5b8299(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81cd2bf9ce39e95cf2e157f89b548b46188b522e5e945c54663937820c77ba0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477a58d75bbe0825289f7f9fe107b3a5a7baac84bd0298d06bf3a5cfbf1879e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8438d3641b4d73721e7684e6154e31df81d144bb8e0ab8744f04280f8e48246(
    value: typing.Optional[ComputeHealthCheckHttpHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f6ffbfdc5a67a90c3374511699a0120b1cfd649653ced1ba24bf80825b61c8(
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

def _typecheckingstub__40c459fd98e9e7a8e8d187903da76f93c780d62f0981bd1442ead16fb2a7dd9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b54100a9b0e2150a957ce7c0ae12d1964a1a14d36f7e94368d329c78d456d87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc3aa27beb1823ddbf8f4d39d0727d3f8058466d28d146195dd4eca2a4b309b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15097cf586b53ea646e24abe8056433f5cf5d0fcada48b1c4b762991ae930bf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a5e854da3592d9256aca4b4971668b12c5cb69cc2e3b373d3310b83bc7e96f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6621b33319a96bcae3a35af5aad003c1133a5db4137a3ec8433e2547b4d9daba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6caa6e30a9b3e0c0bd8cbabc6bf51d8334ade7a617007d259d5639e909e597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be4510b82880e31bda2ed76d1982f1e9c186c05a9d71397c750af1db632951d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1c7ae29b5e6c361cf129572ac6c43b1c6e52c50be78f82e4b63527a8021ef8(
    value: typing.Optional[ComputeHealthCheckHttpsHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ccdb6a273fbd00dc3ff9e62d911865f5f6f2d28b9b409105a773fe86ac6620c(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4c7ffd6e9e25e1d2a41d324fa946dd6d93e14be7f17997ada4f10edcb5b06a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0968bb4581781b812c724ff8f572f908803cfba5e8d84f2d6c272ca1e4dec8a1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d285c737146e3eaa2e66d112acc7a10a9108c2a9366db6617ad69d02d7d7b874(
    value: typing.Optional[ComputeHealthCheckLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a628403851d8855265b12b878d510d089f22c6f9d766e9fe14051d4cb67b5acd(
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

def _typecheckingstub__aa19c4832402c62a702baf8fc003f01c1634bd068bb893d808e4d9f002a12450(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0852cca4463c494ede949acb238041563729d3cf3fb29ff1c4017a7bec6c242(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb38c7e2b94e234af3744173a5b0042ed9b3abfef01fda2ad23156c3b733761d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c32c4c65300d62a5b03d81e3ef7295879474f78976cf8c3476f9a150f520ede(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490bd1392ed36307f8739703e1a73e7823065b3cac4db1f2b66d6077f6de915e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d82d321912f05f86157d4910e551bd6c5586739323ae92ff687b8770b160af5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5a134db3a68d7239f2843e76c3bcc026853973fe5f73c5118c3afc89afc06c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ade1b83b37ee7425600aba740fe1d3ce05d1ba292c8402eb48e3885cc62c6e4(
    value: typing.Optional[ComputeHealthCheckSslHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac1cd9e8c8e9adce9a8ad3ec3cdd9eb474713730c5c9b193efa61e3a68a6d03(
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

def _typecheckingstub__38b53d301f4a7494cb72682c9e0b49e7ff3edcccd21f3be950b5d581b34739a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8dd28f9bebc12f1f5082c96967f87182f16ccdc738813b67b1e11786d02bda(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef5cebf304476a20a557b7b59e1c16e95dbf0056054b1bda95b922ef833c977(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ec3308c84b3d69b7336d74539829f2dd9f49c3c4192f8224270bdefad0eb4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22cc92a52f632d9583f57ad901fd6aeee8c9b895107387a8580646fb45a3145d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6013c910bb38680b5a372822188eb7163abb0d1aa008a16994ef3174b6ac0ffc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57285dee17cd98beedc29dd21bb165e98e6ae7eefc3c5717bf7dd5946f99aea3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfcb169c5b5f96ed251079dbb0c20e826e26f4bf3bd780255216dcd86508607(
    value: typing.Optional[ComputeHealthCheckTcpHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89140a119dbcedc86dc5967a8a39dcc71c45e8a1efd173a9a53bc110a22deb29(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36904e39a0ca5eb1024f473324c4aaa735ae48a8b74aa67965055759d6d138cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96fdadee25e74a621c6417002c0bd128953bb2ebc028d27e1c31052e792e9405(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc9527cfe79583c1a9c9e58afafaee93fe37154bf7b367f745f4a1852437186(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5e7a97608780e0e868498c7f2566ad361f4fd5fd327ccf75841e53428c63eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d283a610fa1e50af14cf5ae0d28f0fad94a1d8efa24086df1b18b72557ef4ca6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeHealthCheckTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
