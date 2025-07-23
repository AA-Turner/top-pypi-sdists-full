r'''
# `google_monitoring_uptime_check_config`

Refer to the Terraform Registry for docs: [`google_monitoring_uptime_check_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config).
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


class MonitoringUptimeCheckConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config google_monitoring_uptime_check_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        timeout: builtins.str,
        checker_type: typing.Optional[builtins.str] = None,
        content_matchers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitoringUptimeCheckConfigContentMatchers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http_check: typing.Optional[typing.Union["MonitoringUptimeCheckConfigHttpCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_check_failures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitored_resource: typing.Optional[typing.Union["MonitoringUptimeCheckConfigMonitoredResource", typing.Dict[builtins.str, typing.Any]]] = None,
        period: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        resource_group: typing.Optional[typing.Union["MonitoringUptimeCheckConfigResourceGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        selected_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        synthetic_monitor: typing.Optional[typing.Union["MonitoringUptimeCheckConfigSyntheticMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        tcp_check: typing.Optional[typing.Union["MonitoringUptimeCheckConfigTcpCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["MonitoringUptimeCheckConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config google_monitoring_uptime_check_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: A human-friendly name for the uptime check configuration. The display name should be unique within a Stackdriver Workspace in order to make it easier to identify; however, uniqueness is not enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#display_name MonitoringUptimeCheckConfig#display_name}
        :param timeout: The maximum amount of time to wait for the request to complete (must be between 1 and 60 seconds). `See the accepted formats <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.Duration>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#timeout MonitoringUptimeCheckConfig#timeout}
        :param checker_type: The checker type to use for the check. If the monitored resource type is 'servicedirectory_service', 'checker_type' must be set to 'VPC_CHECKERS'. Possible values: ["STATIC_IP_CHECKERS", "VPC_CHECKERS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#checker_type MonitoringUptimeCheckConfig#checker_type}
        :param content_matchers: content_matchers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#content_matchers MonitoringUptimeCheckConfig#content_matchers}
        :param http_check: http_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#http_check MonitoringUptimeCheckConfig#http_check}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#id MonitoringUptimeCheckConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_check_failures: Specifies whether to log the results of failed probes to Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#log_check_failures MonitoringUptimeCheckConfig#log_check_failures}
        :param monitored_resource: monitored_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#monitored_resource MonitoringUptimeCheckConfig#monitored_resource}
        :param period: How often, in seconds, the uptime check is performed. Currently, the only supported values are 60s (1 minute), 300s (5 minutes), 600s (10 minutes), and 900s (15 minutes). Optional, defaults to 300s. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#period MonitoringUptimeCheckConfig#period}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#project MonitoringUptimeCheckConfig#project}.
        :param resource_group: resource_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#resource_group MonitoringUptimeCheckConfig#resource_group}
        :param selected_regions: The list of regions from which the check will be run. Some regions contain one location, and others contain more than one. If this field is specified, enough regions to include a minimum of 3 locations must be provided, or an error message is returned. Not specifying this field will result in uptime checks running from all regions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#selected_regions MonitoringUptimeCheckConfig#selected_regions}
        :param synthetic_monitor: synthetic_monitor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#synthetic_monitor MonitoringUptimeCheckConfig#synthetic_monitor}
        :param tcp_check: tcp_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#tcp_check MonitoringUptimeCheckConfig#tcp_check}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#timeouts MonitoringUptimeCheckConfig#timeouts}
        :param user_labels: User-supplied key/value data to be used for organizing and identifying the 'UptimeCheckConfig' objects. The field can contain up to 64 entries. Each key and value is limited to 63 Unicode characters or 128 bytes, whichever is smaller. Labels and values can contain only lowercase letters, numerals, underscores, and dashes. Keys must begin with a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#user_labels MonitoringUptimeCheckConfig#user_labels}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22d6bb0db76f3b6481cdacd8b2baaec0caa6d3c2d348efdb43c628bc57f10ef0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitoringUptimeCheckConfigConfig(
            display_name=display_name,
            timeout=timeout,
            checker_type=checker_type,
            content_matchers=content_matchers,
            http_check=http_check,
            id=id,
            log_check_failures=log_check_failures,
            monitored_resource=monitored_resource,
            period=period,
            project=project,
            resource_group=resource_group,
            selected_regions=selected_regions,
            synthetic_monitor=synthetic_monitor,
            tcp_check=tcp_check,
            timeouts=timeouts,
            user_labels=user_labels,
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
        '''Generates CDKTF code for importing a MonitoringUptimeCheckConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MonitoringUptimeCheckConfig to import.
        :param import_from_id: The id of the existing MonitoringUptimeCheckConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MonitoringUptimeCheckConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96303b91ade2ba912ca8c62f34104bfffcd0926fff5bfbdd5241210c206ffe86)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putContentMatchers")
    def put_content_matchers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitoringUptimeCheckConfigContentMatchers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__308c164f5f07c3e529180e0b8d8424c8d85211d088b093902c0b8ec09cb442cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContentMatchers", [value]))

    @jsii.member(jsii_name="putHttpCheck")
    def put_http_check(
        self,
        *,
        accepted_response_status_codes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_info: typing.Optional[typing.Union["MonitoringUptimeCheckConfigHttpCheckAuthInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        body: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        custom_content_type: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mask_headers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
        ping_config: typing.Optional[typing.Union["MonitoringUptimeCheckConfigHttpCheckPingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        request_method: typing.Optional[builtins.str] = None,
        service_agent_authentication: typing.Optional[typing.Union["MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        use_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        validate_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param accepted_response_status_codes: accepted_response_status_codes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#accepted_response_status_codes MonitoringUptimeCheckConfig#accepted_response_status_codes}
        :param auth_info: auth_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#auth_info MonitoringUptimeCheckConfig#auth_info}
        :param body: The request body associated with the HTTP POST request. If 'content_type' is 'URL_ENCODED', the body passed in must be URL-encoded. Users can provide a 'Content-Length' header via the 'headers' field or the API will do so. If the 'request_method' is 'GET' and 'body' is not empty, the API will return an error. The maximum byte size is 1 megabyte. Note - As with all bytes fields JSON representations are base64 encoded. e.g. 'foo=bar' in URL-encoded form is 'foo%3Dbar' and in base64 encoding is 'Zm9vJTI1M0RiYXI='. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#body MonitoringUptimeCheckConfig#body}
        :param content_type: The content type to use for the check. Possible values: ["TYPE_UNSPECIFIED", "URL_ENCODED", "USER_PROVIDED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#content_type MonitoringUptimeCheckConfig#content_type}
        :param custom_content_type: A user provided content type header to use for the check. The invalid configurations outlined in the 'content_type' field apply to custom_content_type', as well as the following 1. 'content_type' is 'URL_ENCODED' and 'custom_content_type' is set. 2. 'content_type' is 'USER_PROVIDED' and 'custom_content_type' is not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#custom_content_type MonitoringUptimeCheckConfig#custom_content_type}
        :param headers: The list of headers to send as part of the uptime check request. If two headers have the same key and different values, they should be entered as a single header, with the value being a comma-separated list of all the desired values as described in `RFC 2616 (page 31) <https://www.w3.org/Protocols/rfc2616/rfc2616.txt>`_. Entering two separate headers with the same key in a Create call will cause the first to be overwritten by the second. The maximum number of headers allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#headers MonitoringUptimeCheckConfig#headers}
        :param mask_headers: Boolean specifying whether to encrypt the header information. Encryption should be specified for any headers related to authentication that you do not wish to be seen when retrieving the configuration. The server will be responsible for encrypting the headers. On Get/List calls, if 'mask_headers' is set to 'true' then the headers will be obscured with '******'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#mask_headers MonitoringUptimeCheckConfig#mask_headers}
        :param path: The path to the page to run the check against. Will be combined with the host (specified within the MonitoredResource) and port to construct the full URL. If the provided path does not begin with '/', a '/' will be prepended automatically. Optional (defaults to '/'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#path MonitoringUptimeCheckConfig#path}
        :param ping_config: ping_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#ping_config MonitoringUptimeCheckConfig#ping_config}
        :param port: The port to the page to run the check against. Will be combined with 'host' (specified within the `'monitored_resource' <#nested_monitored_resource>`_) and path to construct the full URL. Optional (defaults to 80 without SSL, or 443 with SSL). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#port MonitoringUptimeCheckConfig#port}
        :param request_method: The HTTP request method to use for the check. If set to 'METHOD_UNSPECIFIED' then 'request_method' defaults to 'GET'. Default value: "GET" Possible values: ["METHOD_UNSPECIFIED", "GET", "POST"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#request_method MonitoringUptimeCheckConfig#request_method}
        :param service_agent_authentication: service_agent_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#service_agent_authentication MonitoringUptimeCheckConfig#service_agent_authentication}
        :param use_ssl: If true, use HTTPS instead of HTTP to run the check. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#use_ssl MonitoringUptimeCheckConfig#use_ssl}
        :param validate_ssl: Boolean specifying whether to include SSL certificate validation as a part of the Uptime check. Only applies to checks where 'monitored_resource' is set to 'uptime_url'. If 'use_ssl' is 'false', setting 'validate_ssl' to 'true' has no effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#validate_ssl MonitoringUptimeCheckConfig#validate_ssl}
        '''
        value = MonitoringUptimeCheckConfigHttpCheck(
            accepted_response_status_codes=accepted_response_status_codes,
            auth_info=auth_info,
            body=body,
            content_type=content_type,
            custom_content_type=custom_content_type,
            headers=headers,
            mask_headers=mask_headers,
            path=path,
            ping_config=ping_config,
            port=port,
            request_method=request_method,
            service_agent_authentication=service_agent_authentication,
            use_ssl=use_ssl,
            validate_ssl=validate_ssl,
        )

        return typing.cast(None, jsii.invoke(self, "putHttpCheck", [value]))

    @jsii.member(jsii_name="putMonitoredResource")
    def put_monitored_resource(
        self,
        *,
        labels: typing.Mapping[builtins.str, builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param labels: Values for all of the labels listed in the associated monitored resource descriptor. For example, Compute Engine VM instances use the labels 'project_id', 'instance_id', and 'zone'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#labels MonitoringUptimeCheckConfig#labels}
        :param type: The monitored resource type. This field must match the type field of a `'MonitoredResourceDescriptor' <https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.monitoredResourceDescriptors#MonitoredResourceDescriptor>`_ object. For example, the type of a Compute Engine VM instance is 'gce_instance'. For a list of types, see `Monitoring resource types <https://cloud.google.com/monitoring/api/resources>`_ and `Logging resource types <https://cloud.google.com/logging/docs/api/v2/resource-list>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#type MonitoringUptimeCheckConfig#type}
        '''
        value = MonitoringUptimeCheckConfigMonitoredResource(labels=labels, type=type)

        return typing.cast(None, jsii.invoke(self, "putMonitoredResource", [value]))

    @jsii.member(jsii_name="putResourceGroup")
    def put_resource_group(
        self,
        *,
        group_id: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group_id: The group of resources being monitored. Should be the 'name' of a group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#group_id MonitoringUptimeCheckConfig#group_id}
        :param resource_type: The resource type of the group members. Possible values: ["RESOURCE_TYPE_UNSPECIFIED", "INSTANCE", "AWS_ELB_LOAD_BALANCER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#resource_type MonitoringUptimeCheckConfig#resource_type}
        '''
        value = MonitoringUptimeCheckConfigResourceGroup(
            group_id=group_id, resource_type=resource_type
        )

        return typing.cast(None, jsii.invoke(self, "putResourceGroup", [value]))

    @jsii.member(jsii_name="putSyntheticMonitor")
    def put_synthetic_monitor(
        self,
        *,
        cloud_function_v2: typing.Union["MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param cloud_function_v2: cloud_function_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#cloud_function_v2 MonitoringUptimeCheckConfig#cloud_function_v2}
        '''
        value = MonitoringUptimeCheckConfigSyntheticMonitor(
            cloud_function_v2=cloud_function_v2
        )

        return typing.cast(None, jsii.invoke(self, "putSyntheticMonitor", [value]))

    @jsii.member(jsii_name="putTcpCheck")
    def put_tcp_check(
        self,
        *,
        port: jsii.Number,
        ping_config: typing.Optional[typing.Union["MonitoringUptimeCheckConfigTcpCheckPingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param port: The port to the page to run the check against. Will be combined with host (specified within the 'monitored_resource') to construct the full URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#port MonitoringUptimeCheckConfig#port}
        :param ping_config: ping_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#ping_config MonitoringUptimeCheckConfig#ping_config}
        '''
        value = MonitoringUptimeCheckConfigTcpCheck(port=port, ping_config=ping_config)

        return typing.cast(None, jsii.invoke(self, "putTcpCheck", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#create MonitoringUptimeCheckConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#delete MonitoringUptimeCheckConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#update MonitoringUptimeCheckConfig#update}.
        '''
        value = MonitoringUptimeCheckConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCheckerType")
    def reset_checker_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckerType", []))

    @jsii.member(jsii_name="resetContentMatchers")
    def reset_content_matchers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentMatchers", []))

    @jsii.member(jsii_name="resetHttpCheck")
    def reset_http_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpCheck", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogCheckFailures")
    def reset_log_check_failures(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogCheckFailures", []))

    @jsii.member(jsii_name="resetMonitoredResource")
    def reset_monitored_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoredResource", []))

    @jsii.member(jsii_name="resetPeriod")
    def reset_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriod", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetResourceGroup")
    def reset_resource_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroup", []))

    @jsii.member(jsii_name="resetSelectedRegions")
    def reset_selected_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectedRegions", []))

    @jsii.member(jsii_name="resetSyntheticMonitor")
    def reset_synthetic_monitor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyntheticMonitor", []))

    @jsii.member(jsii_name="resetTcpCheck")
    def reset_tcp_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpCheck", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserLabels")
    def reset_user_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserLabels", []))

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
    @jsii.member(jsii_name="contentMatchers")
    def content_matchers(self) -> "MonitoringUptimeCheckConfigContentMatchersList":
        return typing.cast("MonitoringUptimeCheckConfigContentMatchersList", jsii.get(self, "contentMatchers"))

    @builtins.property
    @jsii.member(jsii_name="httpCheck")
    def http_check(self) -> "MonitoringUptimeCheckConfigHttpCheckOutputReference":
        return typing.cast("MonitoringUptimeCheckConfigHttpCheckOutputReference", jsii.get(self, "httpCheck"))

    @builtins.property
    @jsii.member(jsii_name="monitoredResource")
    def monitored_resource(
        self,
    ) -> "MonitoringUptimeCheckConfigMonitoredResourceOutputReference":
        return typing.cast("MonitoringUptimeCheckConfigMonitoredResourceOutputReference", jsii.get(self, "monitoredResource"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    def resource_group(
        self,
    ) -> "MonitoringUptimeCheckConfigResourceGroupOutputReference":
        return typing.cast("MonitoringUptimeCheckConfigResourceGroupOutputReference", jsii.get(self, "resourceGroup"))

    @builtins.property
    @jsii.member(jsii_name="syntheticMonitor")
    def synthetic_monitor(
        self,
    ) -> "MonitoringUptimeCheckConfigSyntheticMonitorOutputReference":
        return typing.cast("MonitoringUptimeCheckConfigSyntheticMonitorOutputReference", jsii.get(self, "syntheticMonitor"))

    @builtins.property
    @jsii.member(jsii_name="tcpCheck")
    def tcp_check(self) -> "MonitoringUptimeCheckConfigTcpCheckOutputReference":
        return typing.cast("MonitoringUptimeCheckConfigTcpCheckOutputReference", jsii.get(self, "tcpCheck"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MonitoringUptimeCheckConfigTimeoutsOutputReference":
        return typing.cast("MonitoringUptimeCheckConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uptimeCheckId")
    def uptime_check_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uptimeCheckId"))

    @builtins.property
    @jsii.member(jsii_name="checkerTypeInput")
    def checker_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "checkerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="contentMatchersInput")
    def content_matchers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitoringUptimeCheckConfigContentMatchers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitoringUptimeCheckConfigContentMatchers"]]], jsii.get(self, "contentMatchersInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="httpCheckInput")
    def http_check_input(
        self,
    ) -> typing.Optional["MonitoringUptimeCheckConfigHttpCheck"]:
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigHttpCheck"], jsii.get(self, "httpCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logCheckFailuresInput")
    def log_check_failures_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logCheckFailuresInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoredResourceInput")
    def monitored_resource_input(
        self,
    ) -> typing.Optional["MonitoringUptimeCheckConfigMonitoredResource"]:
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigMonitoredResource"], jsii.get(self, "monitoredResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="periodInput")
    def period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupInput")
    def resource_group_input(
        self,
    ) -> typing.Optional["MonitoringUptimeCheckConfigResourceGroup"]:
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigResourceGroup"], jsii.get(self, "resourceGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="selectedRegionsInput")
    def selected_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "selectedRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="syntheticMonitorInput")
    def synthetic_monitor_input(
        self,
    ) -> typing.Optional["MonitoringUptimeCheckConfigSyntheticMonitor"]:
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigSyntheticMonitor"], jsii.get(self, "syntheticMonitorInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpCheckInput")
    def tcp_check_input(self) -> typing.Optional["MonitoringUptimeCheckConfigTcpCheck"]:
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigTcpCheck"], jsii.get(self, "tcpCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitoringUptimeCheckConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitoringUptimeCheckConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userLabelsInput")
    def user_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "userLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="checkerType")
    def checker_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "checkerType"))

    @checker_type.setter
    def checker_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d7bb81752ed283bb97e29bf219f2c25e3d31c7549d2703d6553b046ff394b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f4053d6cfe86fb27c9afe89d35f4d21ebefa9b145e9db253435a2542e515d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df1f17ade259a632ca9baf1645b6ec1a160a8f8d6816b6cfd6ae694a26df1a64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logCheckFailures")
    def log_check_failures(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logCheckFailures"))

    @log_check_failures.setter
    def log_check_failures(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9684dde6feac9b235757664ae06e118e045b797a4ba37e99af377c3bfaf7911a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logCheckFailures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "period"))

    @period.setter
    def period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf91fe23d8566c23e763cec977b5bb60c8bb4af33373f781464b2bffcaa1efd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a58ff0c0c8e932ad95e1a4ced6a4b01ba8dd6dc00a0e01a8ac0c1578b54d6bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selectedRegions")
    def selected_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "selectedRegions"))

    @selected_regions.setter
    def selected_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4e496c8345e40f328e9bb649ac59e6b31afd5c0b73e6e929cd0ec6335adf2d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectedRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7964e1fd7fb9e7b9293e2fbcaa2b050d87d9c4d7865972768866785bfc502af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userLabels")
    def user_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "userLabels"))

    @user_labels.setter
    def user_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a98840566b347c2d1c2a6ac3ea29d91e6f9715ed2d128bba5464b62031f3c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userLabels", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "timeout": "timeout",
        "checker_type": "checkerType",
        "content_matchers": "contentMatchers",
        "http_check": "httpCheck",
        "id": "id",
        "log_check_failures": "logCheckFailures",
        "monitored_resource": "monitoredResource",
        "period": "period",
        "project": "project",
        "resource_group": "resourceGroup",
        "selected_regions": "selectedRegions",
        "synthetic_monitor": "syntheticMonitor",
        "tcp_check": "tcpCheck",
        "timeouts": "timeouts",
        "user_labels": "userLabels",
    },
)
class MonitoringUptimeCheckConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        timeout: builtins.str,
        checker_type: typing.Optional[builtins.str] = None,
        content_matchers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitoringUptimeCheckConfigContentMatchers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http_check: typing.Optional[typing.Union["MonitoringUptimeCheckConfigHttpCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_check_failures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitored_resource: typing.Optional[typing.Union["MonitoringUptimeCheckConfigMonitoredResource", typing.Dict[builtins.str, typing.Any]]] = None,
        period: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        resource_group: typing.Optional[typing.Union["MonitoringUptimeCheckConfigResourceGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        selected_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        synthetic_monitor: typing.Optional[typing.Union["MonitoringUptimeCheckConfigSyntheticMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        tcp_check: typing.Optional[typing.Union["MonitoringUptimeCheckConfigTcpCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["MonitoringUptimeCheckConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: A human-friendly name for the uptime check configuration. The display name should be unique within a Stackdriver Workspace in order to make it easier to identify; however, uniqueness is not enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#display_name MonitoringUptimeCheckConfig#display_name}
        :param timeout: The maximum amount of time to wait for the request to complete (must be between 1 and 60 seconds). `See the accepted formats <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.Duration>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#timeout MonitoringUptimeCheckConfig#timeout}
        :param checker_type: The checker type to use for the check. If the monitored resource type is 'servicedirectory_service', 'checker_type' must be set to 'VPC_CHECKERS'. Possible values: ["STATIC_IP_CHECKERS", "VPC_CHECKERS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#checker_type MonitoringUptimeCheckConfig#checker_type}
        :param content_matchers: content_matchers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#content_matchers MonitoringUptimeCheckConfig#content_matchers}
        :param http_check: http_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#http_check MonitoringUptimeCheckConfig#http_check}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#id MonitoringUptimeCheckConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_check_failures: Specifies whether to log the results of failed probes to Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#log_check_failures MonitoringUptimeCheckConfig#log_check_failures}
        :param monitored_resource: monitored_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#monitored_resource MonitoringUptimeCheckConfig#monitored_resource}
        :param period: How often, in seconds, the uptime check is performed. Currently, the only supported values are 60s (1 minute), 300s (5 minutes), 600s (10 minutes), and 900s (15 minutes). Optional, defaults to 300s. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#period MonitoringUptimeCheckConfig#period}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#project MonitoringUptimeCheckConfig#project}.
        :param resource_group: resource_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#resource_group MonitoringUptimeCheckConfig#resource_group}
        :param selected_regions: The list of regions from which the check will be run. Some regions contain one location, and others contain more than one. If this field is specified, enough regions to include a minimum of 3 locations must be provided, or an error message is returned. Not specifying this field will result in uptime checks running from all regions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#selected_regions MonitoringUptimeCheckConfig#selected_regions}
        :param synthetic_monitor: synthetic_monitor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#synthetic_monitor MonitoringUptimeCheckConfig#synthetic_monitor}
        :param tcp_check: tcp_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#tcp_check MonitoringUptimeCheckConfig#tcp_check}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#timeouts MonitoringUptimeCheckConfig#timeouts}
        :param user_labels: User-supplied key/value data to be used for organizing and identifying the 'UptimeCheckConfig' objects. The field can contain up to 64 entries. Each key and value is limited to 63 Unicode characters or 128 bytes, whichever is smaller. Labels and values can contain only lowercase letters, numerals, underscores, and dashes. Keys must begin with a letter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#user_labels MonitoringUptimeCheckConfig#user_labels}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(http_check, dict):
            http_check = MonitoringUptimeCheckConfigHttpCheck(**http_check)
        if isinstance(monitored_resource, dict):
            monitored_resource = MonitoringUptimeCheckConfigMonitoredResource(**monitored_resource)
        if isinstance(resource_group, dict):
            resource_group = MonitoringUptimeCheckConfigResourceGroup(**resource_group)
        if isinstance(synthetic_monitor, dict):
            synthetic_monitor = MonitoringUptimeCheckConfigSyntheticMonitor(**synthetic_monitor)
        if isinstance(tcp_check, dict):
            tcp_check = MonitoringUptimeCheckConfigTcpCheck(**tcp_check)
        if isinstance(timeouts, dict):
            timeouts = MonitoringUptimeCheckConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aebab24830f7cc6e4b2db4f76a5d92a81080265c7fd9b669e2761ca3a023aa8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument checker_type", value=checker_type, expected_type=type_hints["checker_type"])
            check_type(argname="argument content_matchers", value=content_matchers, expected_type=type_hints["content_matchers"])
            check_type(argname="argument http_check", value=http_check, expected_type=type_hints["http_check"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_check_failures", value=log_check_failures, expected_type=type_hints["log_check_failures"])
            check_type(argname="argument monitored_resource", value=monitored_resource, expected_type=type_hints["monitored_resource"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument selected_regions", value=selected_regions, expected_type=type_hints["selected_regions"])
            check_type(argname="argument synthetic_monitor", value=synthetic_monitor, expected_type=type_hints["synthetic_monitor"])
            check_type(argname="argument tcp_check", value=tcp_check, expected_type=type_hints["tcp_check"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_labels", value=user_labels, expected_type=type_hints["user_labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "timeout": timeout,
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
        if checker_type is not None:
            self._values["checker_type"] = checker_type
        if content_matchers is not None:
            self._values["content_matchers"] = content_matchers
        if http_check is not None:
            self._values["http_check"] = http_check
        if id is not None:
            self._values["id"] = id
        if log_check_failures is not None:
            self._values["log_check_failures"] = log_check_failures
        if monitored_resource is not None:
            self._values["monitored_resource"] = monitored_resource
        if period is not None:
            self._values["period"] = period
        if project is not None:
            self._values["project"] = project
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if selected_regions is not None:
            self._values["selected_regions"] = selected_regions
        if synthetic_monitor is not None:
            self._values["synthetic_monitor"] = synthetic_monitor
        if tcp_check is not None:
            self._values["tcp_check"] = tcp_check
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_labels is not None:
            self._values["user_labels"] = user_labels

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
    def display_name(self) -> builtins.str:
        '''A human-friendly name for the uptime check configuration.

        The display name should be unique within a Stackdriver Workspace in order to make it easier to identify; however, uniqueness is not enforced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#display_name MonitoringUptimeCheckConfig#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timeout(self) -> builtins.str:
        '''The maximum amount of time to wait for the request to complete (must be between 1 and 60 seconds).

        `See the accepted formats <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.Duration>`_

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#timeout MonitoringUptimeCheckConfig#timeout}
        '''
        result = self._values.get("timeout")
        assert result is not None, "Required property 'timeout' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def checker_type(self) -> typing.Optional[builtins.str]:
        '''The checker type to use for the check.

        If the monitored resource type is 'servicedirectory_service', 'checker_type' must be set to 'VPC_CHECKERS'. Possible values: ["STATIC_IP_CHECKERS", "VPC_CHECKERS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#checker_type MonitoringUptimeCheckConfig#checker_type}
        '''
        result = self._values.get("checker_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_matchers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitoringUptimeCheckConfigContentMatchers"]]]:
        '''content_matchers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#content_matchers MonitoringUptimeCheckConfig#content_matchers}
        '''
        result = self._values.get("content_matchers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitoringUptimeCheckConfigContentMatchers"]]], result)

    @builtins.property
    def http_check(self) -> typing.Optional["MonitoringUptimeCheckConfigHttpCheck"]:
        '''http_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#http_check MonitoringUptimeCheckConfig#http_check}
        '''
        result = self._values.get("http_check")
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigHttpCheck"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#id MonitoringUptimeCheckConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_check_failures(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to log the results of failed probes to Cloud Logging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#log_check_failures MonitoringUptimeCheckConfig#log_check_failures}
        '''
        result = self._values.get("log_check_failures")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monitored_resource(
        self,
    ) -> typing.Optional["MonitoringUptimeCheckConfigMonitoredResource"]:
        '''monitored_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#monitored_resource MonitoringUptimeCheckConfig#monitored_resource}
        '''
        result = self._values.get("monitored_resource")
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigMonitoredResource"], result)

    @builtins.property
    def period(self) -> typing.Optional[builtins.str]:
        '''How often, in seconds, the uptime check is performed.

        Currently, the only supported values are 60s (1 minute), 300s (5 minutes), 600s (10 minutes), and 900s (15 minutes). Optional, defaults to 300s.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#period MonitoringUptimeCheckConfig#period}
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#project MonitoringUptimeCheckConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_group(
        self,
    ) -> typing.Optional["MonitoringUptimeCheckConfigResourceGroup"]:
        '''resource_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#resource_group MonitoringUptimeCheckConfig#resource_group}
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigResourceGroup"], result)

    @builtins.property
    def selected_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of regions from which the check will be run.

        Some regions contain one location, and others contain more than one. If this field is specified, enough regions to include a minimum of 3 locations must be provided, or an error message is returned. Not specifying this field will result in uptime checks running from all regions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#selected_regions MonitoringUptimeCheckConfig#selected_regions}
        '''
        result = self._values.get("selected_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def synthetic_monitor(
        self,
    ) -> typing.Optional["MonitoringUptimeCheckConfigSyntheticMonitor"]:
        '''synthetic_monitor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#synthetic_monitor MonitoringUptimeCheckConfig#synthetic_monitor}
        '''
        result = self._values.get("synthetic_monitor")
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigSyntheticMonitor"], result)

    @builtins.property
    def tcp_check(self) -> typing.Optional["MonitoringUptimeCheckConfigTcpCheck"]:
        '''tcp_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#tcp_check MonitoringUptimeCheckConfig#tcp_check}
        '''
        result = self._values.get("tcp_check")
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigTcpCheck"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MonitoringUptimeCheckConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#timeouts MonitoringUptimeCheckConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigTimeouts"], result)

    @builtins.property
    def user_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-supplied key/value data to be used for organizing and identifying the 'UptimeCheckConfig' objects.

        The field can contain up to 64 entries. Each key and value is limited to 63 Unicode characters or 128 bytes, whichever is smaller. Labels and values can contain only lowercase letters, numerals, underscores, and dashes. Keys must begin with a letter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#user_labels MonitoringUptimeCheckConfig#user_labels}
        '''
        result = self._values.get("user_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringUptimeCheckConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigContentMatchers",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "json_path_matcher": "jsonPathMatcher",
        "matcher": "matcher",
    },
)
class MonitoringUptimeCheckConfigContentMatchers:
    def __init__(
        self,
        *,
        content: builtins.str,
        json_path_matcher: typing.Optional[typing.Union["MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher", typing.Dict[builtins.str, typing.Any]]] = None,
        matcher: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: String or regex content to match (max 1024 bytes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#content MonitoringUptimeCheckConfig#content}
        :param json_path_matcher: json_path_matcher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#json_path_matcher MonitoringUptimeCheckConfig#json_path_matcher}
        :param matcher: The type of content matcher that will be applied to the server output, compared to the content string when the check is run. Default value: "CONTAINS_STRING" Possible values: ["CONTAINS_STRING", "NOT_CONTAINS_STRING", "MATCHES_REGEX", "NOT_MATCHES_REGEX", "MATCHES_JSON_PATH", "NOT_MATCHES_JSON_PATH"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#matcher MonitoringUptimeCheckConfig#matcher}
        '''
        if isinstance(json_path_matcher, dict):
            json_path_matcher = MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher(**json_path_matcher)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5d5e0a38ade1b82de9c3706de1ae3020b0e5499d9f72019af7e63bba3c8a326)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument json_path_matcher", value=json_path_matcher, expected_type=type_hints["json_path_matcher"])
            check_type(argname="argument matcher", value=matcher, expected_type=type_hints["matcher"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
        }
        if json_path_matcher is not None:
            self._values["json_path_matcher"] = json_path_matcher
        if matcher is not None:
            self._values["matcher"] = matcher

    @builtins.property
    def content(self) -> builtins.str:
        '''String or regex content to match (max 1024 bytes).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#content MonitoringUptimeCheckConfig#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def json_path_matcher(
        self,
    ) -> typing.Optional["MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher"]:
        '''json_path_matcher block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#json_path_matcher MonitoringUptimeCheckConfig#json_path_matcher}
        '''
        result = self._values.get("json_path_matcher")
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher"], result)

    @builtins.property
    def matcher(self) -> typing.Optional[builtins.str]:
        '''The type of content matcher that will be applied to the server output, compared to the content string when the check is run.

        Default value: "CONTAINS_STRING" Possible values: ["CONTAINS_STRING", "NOT_CONTAINS_STRING", "MATCHES_REGEX", "NOT_MATCHES_REGEX", "MATCHES_JSON_PATH", "NOT_MATCHES_JSON_PATH"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#matcher MonitoringUptimeCheckConfig#matcher}
        '''
        result = self._values.get("matcher")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringUptimeCheckConfigContentMatchers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher",
    jsii_struct_bases=[],
    name_mapping={"json_path": "jsonPath", "json_matcher": "jsonMatcher"},
)
class MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher:
    def __init__(
        self,
        *,
        json_path: builtins.str,
        json_matcher: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param json_path: JSONPath within the response output pointing to the expected 'ContentMatcher::content' to match against. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#json_path MonitoringUptimeCheckConfig#json_path}
        :param json_matcher: Options to perform JSONPath content matching. Default value: "EXACT_MATCH" Possible values: ["EXACT_MATCH", "REGEX_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#json_matcher MonitoringUptimeCheckConfig#json_matcher}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7831f52ff5c5afa8731494eb9e0ef121dc3d5db81b51532233bb60730525ac9d)
            check_type(argname="argument json_path", value=json_path, expected_type=type_hints["json_path"])
            check_type(argname="argument json_matcher", value=json_matcher, expected_type=type_hints["json_matcher"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "json_path": json_path,
        }
        if json_matcher is not None:
            self._values["json_matcher"] = json_matcher

    @builtins.property
    def json_path(self) -> builtins.str:
        '''JSONPath within the response output pointing to the expected 'ContentMatcher::content' to match against.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#json_path MonitoringUptimeCheckConfig#json_path}
        '''
        result = self._values.get("json_path")
        assert result is not None, "Required property 'json_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def json_matcher(self) -> typing.Optional[builtins.str]:
        '''Options to perform JSONPath content matching. Default value: "EXACT_MATCH" Possible values: ["EXACT_MATCH", "REGEX_MATCH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#json_matcher MonitoringUptimeCheckConfig#json_matcher}
        '''
        result = self._values.get("json_matcher")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringUptimeCheckConfigContentMatchersJsonPathMatcherOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigContentMatchersJsonPathMatcherOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__813376971524d5aece7a6e902b6e65b5fd5e44dce60e85c8ddde9464c4356089)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetJsonMatcher")
    def reset_json_matcher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonMatcher", []))

    @builtins.property
    @jsii.member(jsii_name="jsonMatcherInput")
    def json_matcher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jsonMatcherInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonPathInput")
    def json_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jsonPathInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonMatcher")
    def json_matcher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jsonMatcher"))

    @json_matcher.setter
    def json_matcher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81355154d3c1adec0ad5e9279804f73b1e9e71b154f2a200f60bc96f94628ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonMatcher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jsonPath")
    def json_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jsonPath"))

    @json_path.setter
    def json_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff442beff99e5222c36b95b52533d36609d610d17a99ced29e2d261f35434c96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher]:
        return typing.cast(typing.Optional[MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee0ba523ddfdf4db5d7c4e612903c9b2ccf5d843afc9c6022aa901ea2ffd0457)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitoringUptimeCheckConfigContentMatchersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigContentMatchersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9da637ea9032037e38a62e5394942b0c2ab26485c2b8bbbb89212cf4a75a8415)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitoringUptimeCheckConfigContentMatchersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49c8a37797472131d8d072d41f70bec6c2d3ae043d18529e630f36f0e4df553)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitoringUptimeCheckConfigContentMatchersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853513f8ee46a040c493eabb55347796b72b0d84f67319d2901b52849c148112)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56f4dcea86a3e95c4f0d9dae98ced2a579f99be193f1a5ce37c05c4c55068aec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8df91784e4cc57262aecbad54489961dc7eae59ecbbbd2acca8d9c29c66123d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringUptimeCheckConfigContentMatchers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringUptimeCheckConfigContentMatchers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringUptimeCheckConfigContentMatchers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09701864643cd1d2e3c7de07cc835749463ca88ed5a6c60a11ab58a26c4cf340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitoringUptimeCheckConfigContentMatchersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigContentMatchersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be0ba04bfd1e2a4f7a74d983a3a270203e0eec4c1fad9b82710f243cc5071036)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putJsonPathMatcher")
    def put_json_path_matcher(
        self,
        *,
        json_path: builtins.str,
        json_matcher: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param json_path: JSONPath within the response output pointing to the expected 'ContentMatcher::content' to match against. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#json_path MonitoringUptimeCheckConfig#json_path}
        :param json_matcher: Options to perform JSONPath content matching. Default value: "EXACT_MATCH" Possible values: ["EXACT_MATCH", "REGEX_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#json_matcher MonitoringUptimeCheckConfig#json_matcher}
        '''
        value = MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher(
            json_path=json_path, json_matcher=json_matcher
        )

        return typing.cast(None, jsii.invoke(self, "putJsonPathMatcher", [value]))

    @jsii.member(jsii_name="resetJsonPathMatcher")
    def reset_json_path_matcher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonPathMatcher", []))

    @jsii.member(jsii_name="resetMatcher")
    def reset_matcher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatcher", []))

    @builtins.property
    @jsii.member(jsii_name="jsonPathMatcher")
    def json_path_matcher(
        self,
    ) -> MonitoringUptimeCheckConfigContentMatchersJsonPathMatcherOutputReference:
        return typing.cast(MonitoringUptimeCheckConfigContentMatchersJsonPathMatcherOutputReference, jsii.get(self, "jsonPathMatcher"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonPathMatcherInput")
    def json_path_matcher_input(
        self,
    ) -> typing.Optional[MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher]:
        return typing.cast(typing.Optional[MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher], jsii.get(self, "jsonPathMatcherInput"))

    @builtins.property
    @jsii.member(jsii_name="matcherInput")
    def matcher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matcherInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43dd6a401f0862f4b44c7628bde604befa7536df33c2f6213500da8aed848d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matcher")
    def matcher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matcher"))

    @matcher.setter
    def matcher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48bd321d82885c9e23798cf1fc60210d245f07a1286a4daf3a129f7c264b2aff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matcher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringUptimeCheckConfigContentMatchers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringUptimeCheckConfigContentMatchers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringUptimeCheckConfigContentMatchers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c343ad10f66d852dc0b9c839c8d3a891f49d17cd53372d37eaa85b39c64ab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigHttpCheck",
    jsii_struct_bases=[],
    name_mapping={
        "accepted_response_status_codes": "acceptedResponseStatusCodes",
        "auth_info": "authInfo",
        "body": "body",
        "content_type": "contentType",
        "custom_content_type": "customContentType",
        "headers": "headers",
        "mask_headers": "maskHeaders",
        "path": "path",
        "ping_config": "pingConfig",
        "port": "port",
        "request_method": "requestMethod",
        "service_agent_authentication": "serviceAgentAuthentication",
        "use_ssl": "useSsl",
        "validate_ssl": "validateSsl",
    },
)
class MonitoringUptimeCheckConfigHttpCheck:
    def __init__(
        self,
        *,
        accepted_response_status_codes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_info: typing.Optional[typing.Union["MonitoringUptimeCheckConfigHttpCheckAuthInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        body: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        custom_content_type: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mask_headers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
        ping_config: typing.Optional[typing.Union["MonitoringUptimeCheckConfigHttpCheckPingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        request_method: typing.Optional[builtins.str] = None,
        service_agent_authentication: typing.Optional[typing.Union["MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        use_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        validate_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param accepted_response_status_codes: accepted_response_status_codes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#accepted_response_status_codes MonitoringUptimeCheckConfig#accepted_response_status_codes}
        :param auth_info: auth_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#auth_info MonitoringUptimeCheckConfig#auth_info}
        :param body: The request body associated with the HTTP POST request. If 'content_type' is 'URL_ENCODED', the body passed in must be URL-encoded. Users can provide a 'Content-Length' header via the 'headers' field or the API will do so. If the 'request_method' is 'GET' and 'body' is not empty, the API will return an error. The maximum byte size is 1 megabyte. Note - As with all bytes fields JSON representations are base64 encoded. e.g. 'foo=bar' in URL-encoded form is 'foo%3Dbar' and in base64 encoding is 'Zm9vJTI1M0RiYXI='. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#body MonitoringUptimeCheckConfig#body}
        :param content_type: The content type to use for the check. Possible values: ["TYPE_UNSPECIFIED", "URL_ENCODED", "USER_PROVIDED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#content_type MonitoringUptimeCheckConfig#content_type}
        :param custom_content_type: A user provided content type header to use for the check. The invalid configurations outlined in the 'content_type' field apply to custom_content_type', as well as the following 1. 'content_type' is 'URL_ENCODED' and 'custom_content_type' is set. 2. 'content_type' is 'USER_PROVIDED' and 'custom_content_type' is not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#custom_content_type MonitoringUptimeCheckConfig#custom_content_type}
        :param headers: The list of headers to send as part of the uptime check request. If two headers have the same key and different values, they should be entered as a single header, with the value being a comma-separated list of all the desired values as described in `RFC 2616 (page 31) <https://www.w3.org/Protocols/rfc2616/rfc2616.txt>`_. Entering two separate headers with the same key in a Create call will cause the first to be overwritten by the second. The maximum number of headers allowed is 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#headers MonitoringUptimeCheckConfig#headers}
        :param mask_headers: Boolean specifying whether to encrypt the header information. Encryption should be specified for any headers related to authentication that you do not wish to be seen when retrieving the configuration. The server will be responsible for encrypting the headers. On Get/List calls, if 'mask_headers' is set to 'true' then the headers will be obscured with '******'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#mask_headers MonitoringUptimeCheckConfig#mask_headers}
        :param path: The path to the page to run the check against. Will be combined with the host (specified within the MonitoredResource) and port to construct the full URL. If the provided path does not begin with '/', a '/' will be prepended automatically. Optional (defaults to '/'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#path MonitoringUptimeCheckConfig#path}
        :param ping_config: ping_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#ping_config MonitoringUptimeCheckConfig#ping_config}
        :param port: The port to the page to run the check against. Will be combined with 'host' (specified within the `'monitored_resource' <#nested_monitored_resource>`_) and path to construct the full URL. Optional (defaults to 80 without SSL, or 443 with SSL). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#port MonitoringUptimeCheckConfig#port}
        :param request_method: The HTTP request method to use for the check. If set to 'METHOD_UNSPECIFIED' then 'request_method' defaults to 'GET'. Default value: "GET" Possible values: ["METHOD_UNSPECIFIED", "GET", "POST"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#request_method MonitoringUptimeCheckConfig#request_method}
        :param service_agent_authentication: service_agent_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#service_agent_authentication MonitoringUptimeCheckConfig#service_agent_authentication}
        :param use_ssl: If true, use HTTPS instead of HTTP to run the check. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#use_ssl MonitoringUptimeCheckConfig#use_ssl}
        :param validate_ssl: Boolean specifying whether to include SSL certificate validation as a part of the Uptime check. Only applies to checks where 'monitored_resource' is set to 'uptime_url'. If 'use_ssl' is 'false', setting 'validate_ssl' to 'true' has no effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#validate_ssl MonitoringUptimeCheckConfig#validate_ssl}
        '''
        if isinstance(auth_info, dict):
            auth_info = MonitoringUptimeCheckConfigHttpCheckAuthInfo(**auth_info)
        if isinstance(ping_config, dict):
            ping_config = MonitoringUptimeCheckConfigHttpCheckPingConfig(**ping_config)
        if isinstance(service_agent_authentication, dict):
            service_agent_authentication = MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication(**service_agent_authentication)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa000a907aed1339d07ed4f8726f16ed6f3f9cb9e0f3a33740d23c3baed5a01)
            check_type(argname="argument accepted_response_status_codes", value=accepted_response_status_codes, expected_type=type_hints["accepted_response_status_codes"])
            check_type(argname="argument auth_info", value=auth_info, expected_type=type_hints["auth_info"])
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument custom_content_type", value=custom_content_type, expected_type=type_hints["custom_content_type"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument mask_headers", value=mask_headers, expected_type=type_hints["mask_headers"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument ping_config", value=ping_config, expected_type=type_hints["ping_config"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument request_method", value=request_method, expected_type=type_hints["request_method"])
            check_type(argname="argument service_agent_authentication", value=service_agent_authentication, expected_type=type_hints["service_agent_authentication"])
            check_type(argname="argument use_ssl", value=use_ssl, expected_type=type_hints["use_ssl"])
            check_type(argname="argument validate_ssl", value=validate_ssl, expected_type=type_hints["validate_ssl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accepted_response_status_codes is not None:
            self._values["accepted_response_status_codes"] = accepted_response_status_codes
        if auth_info is not None:
            self._values["auth_info"] = auth_info
        if body is not None:
            self._values["body"] = body
        if content_type is not None:
            self._values["content_type"] = content_type
        if custom_content_type is not None:
            self._values["custom_content_type"] = custom_content_type
        if headers is not None:
            self._values["headers"] = headers
        if mask_headers is not None:
            self._values["mask_headers"] = mask_headers
        if path is not None:
            self._values["path"] = path
        if ping_config is not None:
            self._values["ping_config"] = ping_config
        if port is not None:
            self._values["port"] = port
        if request_method is not None:
            self._values["request_method"] = request_method
        if service_agent_authentication is not None:
            self._values["service_agent_authentication"] = service_agent_authentication
        if use_ssl is not None:
            self._values["use_ssl"] = use_ssl
        if validate_ssl is not None:
            self._values["validate_ssl"] = validate_ssl

    @builtins.property
    def accepted_response_status_codes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes"]]]:
        '''accepted_response_status_codes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#accepted_response_status_codes MonitoringUptimeCheckConfig#accepted_response_status_codes}
        '''
        result = self._values.get("accepted_response_status_codes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes"]]], result)

    @builtins.property
    def auth_info(
        self,
    ) -> typing.Optional["MonitoringUptimeCheckConfigHttpCheckAuthInfo"]:
        '''auth_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#auth_info MonitoringUptimeCheckConfig#auth_info}
        '''
        result = self._values.get("auth_info")
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigHttpCheckAuthInfo"], result)

    @builtins.property
    def body(self) -> typing.Optional[builtins.str]:
        '''The request body associated with the HTTP POST request.

        If 'content_type' is 'URL_ENCODED', the body passed in must be URL-encoded. Users can provide a 'Content-Length' header via the 'headers' field or the API will do so. If the 'request_method' is 'GET' and 'body' is not empty, the API will return an error. The maximum byte size is 1 megabyte. Note - As with all bytes fields JSON representations are base64 encoded. e.g. 'foo=bar' in URL-encoded form is 'foo%3Dbar' and in base64 encoding is 'Zm9vJTI1M0RiYXI='.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#body MonitoringUptimeCheckConfig#body}
        '''
        result = self._values.get("body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''The content type to use for the check. Possible values: ["TYPE_UNSPECIFIED", "URL_ENCODED", "USER_PROVIDED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#content_type MonitoringUptimeCheckConfig#content_type}
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_content_type(self) -> typing.Optional[builtins.str]:
        '''A user provided content type header to use for the check.

        The invalid configurations outlined in the 'content_type' field apply to custom_content_type', as well as the following 1. 'content_type' is 'URL_ENCODED' and 'custom_content_type' is set. 2. 'content_type' is 'USER_PROVIDED' and 'custom_content_type' is not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#custom_content_type MonitoringUptimeCheckConfig#custom_content_type}
        '''
        result = self._values.get("custom_content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The list of headers to send as part of the uptime check request.

        If two headers have the same key and different values, they should be entered as a single header, with the value being a comma-separated list of all the desired values as described in `RFC 2616 (page 31) <https://www.w3.org/Protocols/rfc2616/rfc2616.txt>`_. Entering two separate headers with the same key in a Create call will cause the first to be overwritten by the second. The maximum number of headers allowed is 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#headers MonitoringUptimeCheckConfig#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mask_headers(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean specifying whether to encrypt the header information.

        Encryption should be specified for any headers related to authentication that you do not wish to be seen when retrieving the configuration. The server will be responsible for encrypting the headers. On Get/List calls, if 'mask_headers' is set to 'true' then the headers will be obscured with '******'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#mask_headers MonitoringUptimeCheckConfig#mask_headers}
        '''
        result = self._values.get("mask_headers")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the page to run the check against.

        Will be combined with the host (specified within the MonitoredResource) and port to construct the full URL. If the provided path does not begin with '/', a '/' will be prepended automatically. Optional (defaults to '/').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#path MonitoringUptimeCheckConfig#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ping_config(
        self,
    ) -> typing.Optional["MonitoringUptimeCheckConfigHttpCheckPingConfig"]:
        '''ping_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#ping_config MonitoringUptimeCheckConfig#ping_config}
        '''
        result = self._values.get("ping_config")
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigHttpCheckPingConfig"], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port to the page to run the check against.

        Will be combined with 'host' (specified within the `'monitored_resource' <#nested_monitored_resource>`_) and path to construct the full URL. Optional (defaults to 80 without SSL, or 443 with SSL).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#port MonitoringUptimeCheckConfig#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def request_method(self) -> typing.Optional[builtins.str]:
        '''The HTTP request method to use for the check.

        If set to 'METHOD_UNSPECIFIED' then 'request_method' defaults to 'GET'. Default value: "GET" Possible values: ["METHOD_UNSPECIFIED", "GET", "POST"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#request_method MonitoringUptimeCheckConfig#request_method}
        '''
        result = self._values.get("request_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_agent_authentication(
        self,
    ) -> typing.Optional["MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication"]:
        '''service_agent_authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#service_agent_authentication MonitoringUptimeCheckConfig#service_agent_authentication}
        '''
        result = self._values.get("service_agent_authentication")
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication"], result)

    @builtins.property
    def use_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, use HTTPS instead of HTTP to run the check.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#use_ssl MonitoringUptimeCheckConfig#use_ssl}
        '''
        result = self._values.get("use_ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def validate_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean specifying whether to include SSL certificate validation as a part of the Uptime check.

        Only applies to checks where 'monitored_resource' is set to 'uptime_url'. If 'use_ssl' is 'false', setting 'validate_ssl' to 'true' has no effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#validate_ssl MonitoringUptimeCheckConfig#validate_ssl}
        '''
        result = self._values.get("validate_ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringUptimeCheckConfigHttpCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes",
    jsii_struct_bases=[],
    name_mapping={"status_class": "statusClass", "status_value": "statusValue"},
)
class MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes:
    def __init__(
        self,
        *,
        status_class: typing.Optional[builtins.str] = None,
        status_value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param status_class: A class of status codes to accept. Possible values: ["STATUS_CLASS_1XX", "STATUS_CLASS_2XX", "STATUS_CLASS_3XX", "STATUS_CLASS_4XX", "STATUS_CLASS_5XX", "STATUS_CLASS_ANY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#status_class MonitoringUptimeCheckConfig#status_class}
        :param status_value: A status code to accept. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#status_value MonitoringUptimeCheckConfig#status_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4865d480af3b8d146894971da216ed8dd30d65bd11d31c9281b084cabe5a144)
            check_type(argname="argument status_class", value=status_class, expected_type=type_hints["status_class"])
            check_type(argname="argument status_value", value=status_value, expected_type=type_hints["status_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if status_class is not None:
            self._values["status_class"] = status_class
        if status_value is not None:
            self._values["status_value"] = status_value

    @builtins.property
    def status_class(self) -> typing.Optional[builtins.str]:
        '''A class of status codes to accept. Possible values: ["STATUS_CLASS_1XX", "STATUS_CLASS_2XX", "STATUS_CLASS_3XX", "STATUS_CLASS_4XX", "STATUS_CLASS_5XX", "STATUS_CLASS_ANY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#status_class MonitoringUptimeCheckConfig#status_class}
        '''
        result = self._values.get("status_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status_value(self) -> typing.Optional[jsii.Number]:
        '''A status code to accept.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#status_value MonitoringUptimeCheckConfig#status_value}
        '''
        result = self._values.get("status_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3d56f5962b23dc713f0ffa75909b84c3c27ca36b276645af3825ec397d6c3ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0dba9f7d78303d051e0cf071bcdae54fb567f6fc292010e10bfed0320ec1868)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__813a610fb8d07aeda6a6857c3427d61840c50fac217bb9bcca625e60d57e9b67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4b061d6c28f7ef564382e03d5663c41ab37692e7baf72ed6654157e1f83cabe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab4925490417d772c9c004f1a3dffb900d83a52bf4cef790281d70f4b35bdba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a3b2b62e0947bf5e9ef13c6384af176453eb2138943ab81b86a3008ad3cef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1082bf5437143b8d7ed3d6b0dce78bf9a4a32d728c16908b6d7cd19d68197c87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetStatusClass")
    def reset_status_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatusClass", []))

    @jsii.member(jsii_name="resetStatusValue")
    def reset_status_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatusValue", []))

    @builtins.property
    @jsii.member(jsii_name="statusClassInput")
    def status_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusClassInput"))

    @builtins.property
    @jsii.member(jsii_name="statusValueInput")
    def status_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statusValueInput"))

    @builtins.property
    @jsii.member(jsii_name="statusClass")
    def status_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusClass"))

    @status_class.setter
    def status_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df7e557e4c503a29081c1fb7e4e56b315f743c591de5ea155437f7c85d67045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statusValue")
    def status_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statusValue"))

    @status_value.setter
    def status_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a276ffd2a41cea8612210dad752d57e8005c20cf7995282f29c9c556fd578912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae7ddb80723d9da12276766927d24ea8dc3d3c0e5e29ba6c1b55dee366f4d568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigHttpCheckAuthInfo",
    jsii_struct_bases=[],
    name_mapping={
        "username": "username",
        "password": "password",
        "password_wo": "passwordWo",
        "password_wo_version": "passwordWoVersion",
    },
)
class MonitoringUptimeCheckConfigHttpCheckAuthInfo:
    def __init__(
        self,
        *,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
        password_wo: typing.Optional[builtins.str] = None,
        password_wo_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: The username to authenticate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#username MonitoringUptimeCheckConfig#username}
        :param password: The password to authenticate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#password MonitoringUptimeCheckConfig#password}
        :param password_wo: The password to authenticate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#password_wo MonitoringUptimeCheckConfig#password_wo}
        :param password_wo_version: The password write-only version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#password_wo_version MonitoringUptimeCheckConfig#password_wo_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b002f871fd2676a9251fc5e0d16bf6af6fc5d857a07a5252ace1d680d6768d0)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument password_wo", value=password_wo, expected_type=type_hints["password_wo"])
            check_type(argname="argument password_wo_version", value=password_wo_version, expected_type=type_hints["password_wo_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }
        if password is not None:
            self._values["password"] = password
        if password_wo is not None:
            self._values["password_wo"] = password_wo
        if password_wo_version is not None:
            self._values["password_wo_version"] = password_wo_version

    @builtins.property
    def username(self) -> builtins.str:
        '''The username to authenticate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#username MonitoringUptimeCheckConfig#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The password to authenticate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#password MonitoringUptimeCheckConfig#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password_wo(self) -> typing.Optional[builtins.str]:
        '''The password to authenticate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#password_wo MonitoringUptimeCheckConfig#password_wo}
        '''
        result = self._values.get("password_wo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password_wo_version(self) -> typing.Optional[builtins.str]:
        '''The password write-only version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#password_wo_version MonitoringUptimeCheckConfig#password_wo_version}
        '''
        result = self._values.get("password_wo_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringUptimeCheckConfigHttpCheckAuthInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringUptimeCheckConfigHttpCheckAuthInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigHttpCheckAuthInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92e76bfcd9df7a2e362fd69bd7db677cccc6dedd18ea10fdc2b2cf9d55856458)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPasswordWo")
    def reset_password_wo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordWo", []))

    @jsii.member(jsii_name="resetPasswordWoVersion")
    def reset_password_wo_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordWoVersion", []))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordWoInput")
    def password_wo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordWoInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordWoVersionInput")
    def password_wo_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordWoVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c63901d2e3a2e4e59c1867e911089dda5353f6804ec1814fce15440bf37948e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordWo")
    def password_wo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordWo"))

    @password_wo.setter
    def password_wo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5bd482f3c39109f63aeec446f2248b7611507faeb0af2ee6285ceda7a9bbcc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordWo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordWoVersion")
    def password_wo_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordWoVersion"))

    @password_wo_version.setter
    def password_wo_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c09e56737505038801027505774a4d7aaa3a1acc5af112cb534b62ceb2c31a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordWoVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__894134ddcf72e731262d775bd895cf6fc600371bedddd79b2219b75d0284592a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringUptimeCheckConfigHttpCheckAuthInfo]:
        return typing.cast(typing.Optional[MonitoringUptimeCheckConfigHttpCheckAuthInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringUptimeCheckConfigHttpCheckAuthInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077f182a7be5152b622bb7d649f7e7cd7d433bd5f175533abc390c8b2b0b337e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitoringUptimeCheckConfigHttpCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigHttpCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36c21a00172d3ee361100efa5506a3b7565ed34f6004c4f692e220341977e16a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAcceptedResponseStatusCodes")
    def put_accepted_response_status_codes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff28f71fb3aefeef9815aa4b6ebd3184e10850b32248eff242102275b35145c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAcceptedResponseStatusCodes", [value]))

    @jsii.member(jsii_name="putAuthInfo")
    def put_auth_info(
        self,
        *,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
        password_wo: typing.Optional[builtins.str] = None,
        password_wo_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: The username to authenticate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#username MonitoringUptimeCheckConfig#username}
        :param password: The password to authenticate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#password MonitoringUptimeCheckConfig#password}
        :param password_wo: The password to authenticate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#password_wo MonitoringUptimeCheckConfig#password_wo}
        :param password_wo_version: The password write-only version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#password_wo_version MonitoringUptimeCheckConfig#password_wo_version}
        '''
        value = MonitoringUptimeCheckConfigHttpCheckAuthInfo(
            username=username,
            password=password,
            password_wo=password_wo,
            password_wo_version=password_wo_version,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthInfo", [value]))

    @jsii.member(jsii_name="putPingConfig")
    def put_ping_config(self, *, pings_count: jsii.Number) -> None:
        '''
        :param pings_count: Number of ICMP pings. A maximum of 3 ICMP pings is currently supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#pings_count MonitoringUptimeCheckConfig#pings_count}
        '''
        value = MonitoringUptimeCheckConfigHttpCheckPingConfig(pings_count=pings_count)

        return typing.cast(None, jsii.invoke(self, "putPingConfig", [value]))

    @jsii.member(jsii_name="putServiceAgentAuthentication")
    def put_service_agent_authentication(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: The type of authentication to use. Possible values: ["SERVICE_AGENT_AUTHENTICATION_TYPE_UNSPECIFIED", "OIDC_TOKEN"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#type MonitoringUptimeCheckConfig#type}
        '''
        value = MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication(
            type=type
        )

        return typing.cast(None, jsii.invoke(self, "putServiceAgentAuthentication", [value]))

    @jsii.member(jsii_name="resetAcceptedResponseStatusCodes")
    def reset_accepted_response_status_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceptedResponseStatusCodes", []))

    @jsii.member(jsii_name="resetAuthInfo")
    def reset_auth_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthInfo", []))

    @jsii.member(jsii_name="resetBody")
    def reset_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBody", []))

    @jsii.member(jsii_name="resetContentType")
    def reset_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentType", []))

    @jsii.member(jsii_name="resetCustomContentType")
    def reset_custom_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomContentType", []))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetMaskHeaders")
    def reset_mask_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaskHeaders", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPingConfig")
    def reset_ping_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPingConfig", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetRequestMethod")
    def reset_request_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestMethod", []))

    @jsii.member(jsii_name="resetServiceAgentAuthentication")
    def reset_service_agent_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAgentAuthentication", []))

    @jsii.member(jsii_name="resetUseSsl")
    def reset_use_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseSsl", []))

    @jsii.member(jsii_name="resetValidateSsl")
    def reset_validate_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidateSsl", []))

    @builtins.property
    @jsii.member(jsii_name="acceptedResponseStatusCodes")
    def accepted_response_status_codes(
        self,
    ) -> MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodesList:
        return typing.cast(MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodesList, jsii.get(self, "acceptedResponseStatusCodes"))

    @builtins.property
    @jsii.member(jsii_name="authInfo")
    def auth_info(self) -> MonitoringUptimeCheckConfigHttpCheckAuthInfoOutputReference:
        return typing.cast(MonitoringUptimeCheckConfigHttpCheckAuthInfoOutputReference, jsii.get(self, "authInfo"))

    @builtins.property
    @jsii.member(jsii_name="pingConfig")
    def ping_config(
        self,
    ) -> "MonitoringUptimeCheckConfigHttpCheckPingConfigOutputReference":
        return typing.cast("MonitoringUptimeCheckConfigHttpCheckPingConfigOutputReference", jsii.get(self, "pingConfig"))

    @builtins.property
    @jsii.member(jsii_name="serviceAgentAuthentication")
    def service_agent_authentication(
        self,
    ) -> "MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthenticationOutputReference":
        return typing.cast("MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthenticationOutputReference", jsii.get(self, "serviceAgentAuthentication"))

    @builtins.property
    @jsii.member(jsii_name="acceptedResponseStatusCodesInput")
    def accepted_response_status_codes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes]]], jsii.get(self, "acceptedResponseStatusCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="authInfoInput")
    def auth_info_input(
        self,
    ) -> typing.Optional[MonitoringUptimeCheckConfigHttpCheckAuthInfo]:
        return typing.cast(typing.Optional[MonitoringUptimeCheckConfigHttpCheckAuthInfo], jsii.get(self, "authInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyInput")
    def body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="customContentTypeInput")
    def custom_content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customContentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="maskHeadersInput")
    def mask_headers_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "maskHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="pingConfigInput")
    def ping_config_input(
        self,
    ) -> typing.Optional["MonitoringUptimeCheckConfigHttpCheckPingConfig"]:
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigHttpCheckPingConfig"], jsii.get(self, "pingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="requestMethodInput")
    def request_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAgentAuthenticationInput")
    def service_agent_authentication_input(
        self,
    ) -> typing.Optional["MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication"]:
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication"], jsii.get(self, "serviceAgentAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="useSslInput")
    def use_ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useSslInput"))

    @builtins.property
    @jsii.member(jsii_name="validateSslInput")
    def validate_ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "validateSslInput"))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @body.setter
    def body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40676f8cc05dd594dca2fba8a0a5fb5fcd8dae1d62bd2fba43f98976fc54e9b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "body", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__021b232f7b07e98b9df8c9feaf3dd7d60569490ee7bbb44ce3d6835b9c49af9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customContentType")
    def custom_content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customContentType"))

    @custom_content_type.setter
    def custom_content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99dfa8cc51520859ad7afc8719acdc48c7223523aa83c2d75d4c435394b63eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customContentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "headers"))

    @headers.setter
    def headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea1033c129ad7a29ab4d95a6f285d1b75f9f0841b507d16636f0cd152ce3adda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maskHeaders")
    def mask_headers(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "maskHeaders"))

    @mask_headers.setter
    def mask_headers(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2f5eb2045b8b1be108160fdcf224a6240a0dc3677ea875d468fee831e565d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maskHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b50bdc7807579cb466679f1a1ff8c87d024c25138685be32287e74cfba8e70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ba4dcecf05b1a5c046729882b73554f1a01039e1cd4c0b152fdfcbdc9c1c0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestMethod")
    def request_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestMethod"))

    @request_method.setter
    def request_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e2d5a3200d25e54e5fab6e269b346df50b16d78c675ab67841d8f9642e67c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useSsl")
    def use_ssl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useSsl"))

    @use_ssl.setter
    def use_ssl(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9a641833fc63dec5771d9c0fcb49a4963de009c80041fad59abce4eab713f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useSsl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validateSsl")
    def validate_ssl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "validateSsl"))

    @validate_ssl.setter
    def validate_ssl(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9da645f5fbeea09606bd68b62e432dbec87853c7e0c990b0473d708901769ef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validateSsl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitoringUptimeCheckConfigHttpCheck]:
        return typing.cast(typing.Optional[MonitoringUptimeCheckConfigHttpCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringUptimeCheckConfigHttpCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f259a1cae23cb893e2316de7fbd5803aee1e3e8916bb248621985a2a5e9a3af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigHttpCheckPingConfig",
    jsii_struct_bases=[],
    name_mapping={"pings_count": "pingsCount"},
)
class MonitoringUptimeCheckConfigHttpCheckPingConfig:
    def __init__(self, *, pings_count: jsii.Number) -> None:
        '''
        :param pings_count: Number of ICMP pings. A maximum of 3 ICMP pings is currently supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#pings_count MonitoringUptimeCheckConfig#pings_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9393784c6207b165f26d296ca9ca60877d5017cb7ded18ab7759f86bea6d75)
            check_type(argname="argument pings_count", value=pings_count, expected_type=type_hints["pings_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pings_count": pings_count,
        }

    @builtins.property
    def pings_count(self) -> jsii.Number:
        '''Number of ICMP pings. A maximum of 3 ICMP pings is currently supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#pings_count MonitoringUptimeCheckConfig#pings_count}
        '''
        result = self._values.get("pings_count")
        assert result is not None, "Required property 'pings_count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringUptimeCheckConfigHttpCheckPingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringUptimeCheckConfigHttpCheckPingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigHttpCheckPingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a51d967d069ca7df14d2b17aee677e1e2db9d6ae5d2162d142c48169529c0f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="pingsCountInput")
    def pings_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pingsCountInput"))

    @builtins.property
    @jsii.member(jsii_name="pingsCount")
    def pings_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pingsCount"))

    @pings_count.setter
    def pings_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08fcb22f63194a27ac581e758cbb09d2bfb57ef12283b9e7513411ca5e3ce927)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pingsCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringUptimeCheckConfigHttpCheckPingConfig]:
        return typing.cast(typing.Optional[MonitoringUptimeCheckConfigHttpCheckPingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringUptimeCheckConfigHttpCheckPingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa045d073e77b8db4088ff4cfa787923bddd718fc2995bba4f1915301a083ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication:
    def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param type: The type of authentication to use. Possible values: ["SERVICE_AGENT_AUTHENTICATION_TYPE_UNSPECIFIED", "OIDC_TOKEN"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#type MonitoringUptimeCheckConfig#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797e498aa4f065f2c8b66236b8dc9b4d81d1efc1bf316219c014b20a0bf58b04)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of authentication to use. Possible values: ["SERVICE_AGENT_AUTHENTICATION_TYPE_UNSPECIFIED", "OIDC_TOKEN"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#type MonitoringUptimeCheckConfig#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38a810b52496d66a9b0d232b5827710a51eaba51328c73482fc19caea69356b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7036d6dbe1fb50cc8a23c8c380391d458771b62b1368c970ae2588b413ed63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication]:
        return typing.cast(typing.Optional[MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b2a7d816997b2f64a3ad7c95d0f637668c5478f87a78632e6b1477b520ac397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigMonitoredResource",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "type": "type"},
)
class MonitoringUptimeCheckConfigMonitoredResource:
    def __init__(
        self,
        *,
        labels: typing.Mapping[builtins.str, builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param labels: Values for all of the labels listed in the associated monitored resource descriptor. For example, Compute Engine VM instances use the labels 'project_id', 'instance_id', and 'zone'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#labels MonitoringUptimeCheckConfig#labels}
        :param type: The monitored resource type. This field must match the type field of a `'MonitoredResourceDescriptor' <https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.monitoredResourceDescriptors#MonitoredResourceDescriptor>`_ object. For example, the type of a Compute Engine VM instance is 'gce_instance'. For a list of types, see `Monitoring resource types <https://cloud.google.com/monitoring/api/resources>`_ and `Logging resource types <https://cloud.google.com/logging/docs/api/v2/resource-list>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#type MonitoringUptimeCheckConfig#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a57ea68e8381a7e5d16034ebd9450191978ee55104d6ab243d0fe1c31124e4)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "labels": labels,
            "type": type,
        }

    @builtins.property
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Values for all of the labels listed in the associated monitored resource descriptor.

        For example, Compute Engine VM instances use the labels 'project_id', 'instance_id', and 'zone'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#labels MonitoringUptimeCheckConfig#labels}
        '''
        result = self._values.get("labels")
        assert result is not None, "Required property 'labels' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The monitored resource type.

        This field must match the type field of a `'MonitoredResourceDescriptor' <https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.monitoredResourceDescriptors#MonitoredResourceDescriptor>`_ object. For example, the type of a Compute Engine VM instance is 'gce_instance'. For a list of types, see `Monitoring resource types <https://cloud.google.com/monitoring/api/resources>`_ and `Logging resource types <https://cloud.google.com/logging/docs/api/v2/resource-list>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#type MonitoringUptimeCheckConfig#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringUptimeCheckConfigMonitoredResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringUptimeCheckConfigMonitoredResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigMonitoredResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05cc776cfb5087225b2e75dc323c995323cf82789df54b7c715fa8f8222ee5f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d9b458d405fd37abb15e4fdd28cb39090e009870269a476cf1de26f82556df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea5e5d1aa63996d8e60ca7be5ee49bc5560f9d41150c3e11b4d851901cc81613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringUptimeCheckConfigMonitoredResource]:
        return typing.cast(typing.Optional[MonitoringUptimeCheckConfigMonitoredResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringUptimeCheckConfigMonitoredResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e6fbb2efce74b900163b90305e58f0a5c42691a50bfea7de3ad857a4793b20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigResourceGroup",
    jsii_struct_bases=[],
    name_mapping={"group_id": "groupId", "resource_type": "resourceType"},
)
class MonitoringUptimeCheckConfigResourceGroup:
    def __init__(
        self,
        *,
        group_id: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group_id: The group of resources being monitored. Should be the 'name' of a group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#group_id MonitoringUptimeCheckConfig#group_id}
        :param resource_type: The resource type of the group members. Possible values: ["RESOURCE_TYPE_UNSPECIFIED", "INSTANCE", "AWS_ELB_LOAD_BALANCER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#resource_type MonitoringUptimeCheckConfig#resource_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f100667c91205d0928732278ba1d7ec789499ca2bd0e0153ade457ef0fe77af9)
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_id is not None:
            self._values["group_id"] = group_id
        if resource_type is not None:
            self._values["resource_type"] = resource_type

    @builtins.property
    def group_id(self) -> typing.Optional[builtins.str]:
        '''The group of resources being monitored. Should be the 'name' of a group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#group_id MonitoringUptimeCheckConfig#group_id}
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''The resource type of the group members. Possible values: ["RESOURCE_TYPE_UNSPECIFIED", "INSTANCE", "AWS_ELB_LOAD_BALANCER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#resource_type MonitoringUptimeCheckConfig#resource_type}
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringUptimeCheckConfigResourceGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringUptimeCheckConfigResourceGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigResourceGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0b1563b42eafc1c052514046b1dc96b9a4bc5b957ccb08d7c0b026dc6efddc2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGroupId")
    def reset_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupId", []))

    @jsii.member(jsii_name="resetResourceType")
    def reset_resource_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceType", []))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43eac06ee4ec61dd5b12d9f04fc5c22538992db5e0ec3839ed95573d0982e586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8af517224eb9d280c9724755e95c24e57eba1c5b6d49a5d9539405547dd2e7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringUptimeCheckConfigResourceGroup]:
        return typing.cast(typing.Optional[MonitoringUptimeCheckConfigResourceGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringUptimeCheckConfigResourceGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a834491cb0b97707e80f95aeef79adb46a123b041f1517112a3a47481c0a5642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigSyntheticMonitor",
    jsii_struct_bases=[],
    name_mapping={"cloud_function_v2": "cloudFunctionV2"},
)
class MonitoringUptimeCheckConfigSyntheticMonitor:
    def __init__(
        self,
        *,
        cloud_function_v2: typing.Union["MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param cloud_function_v2: cloud_function_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#cloud_function_v2 MonitoringUptimeCheckConfig#cloud_function_v2}
        '''
        if isinstance(cloud_function_v2, dict):
            cloud_function_v2 = MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2(**cloud_function_v2)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a024a5207279280261ed4d86546b9af6c81f1f271f2d2de25ff7f3c83a8887)
            check_type(argname="argument cloud_function_v2", value=cloud_function_v2, expected_type=type_hints["cloud_function_v2"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_function_v2": cloud_function_v2,
        }

    @builtins.property
    def cloud_function_v2(
        self,
    ) -> "MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2":
        '''cloud_function_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#cloud_function_v2 MonitoringUptimeCheckConfig#cloud_function_v2}
        '''
        result = self._values.get("cloud_function_v2")
        assert result is not None, "Required property 'cloud_function_v2' is missing"
        return typing.cast("MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringUptimeCheckConfigSyntheticMonitor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: The fully qualified name of the cloud function resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#name MonitoringUptimeCheckConfig#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92fc8a68cedf84bacf306212f95787a8142dbecaf60ee508e168b159a9bca9d9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The fully qualified name of the cloud function resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#name MonitoringUptimeCheckConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f784ed1c14559b6d9a65d0f742d8ee3b9e5b3baba193c43281d31208b2bebb84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea5b8df51c29c2abf5e0c6cc392fe3e781cde2d7b6e81a07d66940be50d0fd26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2]:
        return typing.cast(typing.Optional[MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88acaa2852f0e9d2050dbfba811ab92da10bcadbbf2199e2e45490418eb9559b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitoringUptimeCheckConfigSyntheticMonitorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigSyntheticMonitorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33b3d488661b61e9572a718f7c8dd7103071fa12d7f962ae90fbc66e20a23ac3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudFunctionV2")
    def put_cloud_function_v2(self, *, name: builtins.str) -> None:
        '''
        :param name: The fully qualified name of the cloud function resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#name MonitoringUptimeCheckConfig#name}
        '''
        value = MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2(name=name)

        return typing.cast(None, jsii.invoke(self, "putCloudFunctionV2", [value]))

    @builtins.property
    @jsii.member(jsii_name="cloudFunctionV2")
    def cloud_function_v2(
        self,
    ) -> MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2OutputReference:
        return typing.cast(MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2OutputReference, jsii.get(self, "cloudFunctionV2"))

    @builtins.property
    @jsii.member(jsii_name="cloudFunctionV2Input")
    def cloud_function_v2_input(
        self,
    ) -> typing.Optional[MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2]:
        return typing.cast(typing.Optional[MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2], jsii.get(self, "cloudFunctionV2Input"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringUptimeCheckConfigSyntheticMonitor]:
        return typing.cast(typing.Optional[MonitoringUptimeCheckConfigSyntheticMonitor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringUptimeCheckConfigSyntheticMonitor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0075fbcde952498715f53aa3e177dcaf0a68423017ac8f5118cb51d97aed2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigTcpCheck",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "ping_config": "pingConfig"},
)
class MonitoringUptimeCheckConfigTcpCheck:
    def __init__(
        self,
        *,
        port: jsii.Number,
        ping_config: typing.Optional[typing.Union["MonitoringUptimeCheckConfigTcpCheckPingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param port: The port to the page to run the check against. Will be combined with host (specified within the 'monitored_resource') to construct the full URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#port MonitoringUptimeCheckConfig#port}
        :param ping_config: ping_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#ping_config MonitoringUptimeCheckConfig#ping_config}
        '''
        if isinstance(ping_config, dict):
            ping_config = MonitoringUptimeCheckConfigTcpCheckPingConfig(**ping_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aefdc46fd2e3e339e665901fa9ab5c8ca8d4abd40fdc618af240bc0665d5aacd)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument ping_config", value=ping_config, expected_type=type_hints["ping_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
        }
        if ping_config is not None:
            self._values["ping_config"] = ping_config

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port to the page to run the check against.

        Will be combined with host (specified within the 'monitored_resource') to construct the full URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#port MonitoringUptimeCheckConfig#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def ping_config(
        self,
    ) -> typing.Optional["MonitoringUptimeCheckConfigTcpCheckPingConfig"]:
        '''ping_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#ping_config MonitoringUptimeCheckConfig#ping_config}
        '''
        result = self._values.get("ping_config")
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigTcpCheckPingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringUptimeCheckConfigTcpCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringUptimeCheckConfigTcpCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigTcpCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a7cab9781a672bc648150addc0cbc0fa7dd5cd09914adf936d58ee77bbef1b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPingConfig")
    def put_ping_config(self, *, pings_count: jsii.Number) -> None:
        '''
        :param pings_count: Number of ICMP pings. A maximum of 3 ICMP pings is currently supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#pings_count MonitoringUptimeCheckConfig#pings_count}
        '''
        value = MonitoringUptimeCheckConfigTcpCheckPingConfig(pings_count=pings_count)

        return typing.cast(None, jsii.invoke(self, "putPingConfig", [value]))

    @jsii.member(jsii_name="resetPingConfig")
    def reset_ping_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="pingConfig")
    def ping_config(
        self,
    ) -> "MonitoringUptimeCheckConfigTcpCheckPingConfigOutputReference":
        return typing.cast("MonitoringUptimeCheckConfigTcpCheckPingConfigOutputReference", jsii.get(self, "pingConfig"))

    @builtins.property
    @jsii.member(jsii_name="pingConfigInput")
    def ping_config_input(
        self,
    ) -> typing.Optional["MonitoringUptimeCheckConfigTcpCheckPingConfig"]:
        return typing.cast(typing.Optional["MonitoringUptimeCheckConfigTcpCheckPingConfig"], jsii.get(self, "pingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dcbb07332e613233b2285b4b635cbdf344e427b472aeb6e893d71bf8136f3d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitoringUptimeCheckConfigTcpCheck]:
        return typing.cast(typing.Optional[MonitoringUptimeCheckConfigTcpCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringUptimeCheckConfigTcpCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ab91a68b8012fe5e2be726ccc3014139b4567f2f4c2230c182932cf4989a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigTcpCheckPingConfig",
    jsii_struct_bases=[],
    name_mapping={"pings_count": "pingsCount"},
)
class MonitoringUptimeCheckConfigTcpCheckPingConfig:
    def __init__(self, *, pings_count: jsii.Number) -> None:
        '''
        :param pings_count: Number of ICMP pings. A maximum of 3 ICMP pings is currently supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#pings_count MonitoringUptimeCheckConfig#pings_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95fcdaaa5003ffe6495da67d1384d1c57c1302fad80d128677cf37fb50241a06)
            check_type(argname="argument pings_count", value=pings_count, expected_type=type_hints["pings_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pings_count": pings_count,
        }

    @builtins.property
    def pings_count(self) -> jsii.Number:
        '''Number of ICMP pings. A maximum of 3 ICMP pings is currently supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#pings_count MonitoringUptimeCheckConfig#pings_count}
        '''
        result = self._values.get("pings_count")
        assert result is not None, "Required property 'pings_count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringUptimeCheckConfigTcpCheckPingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringUptimeCheckConfigTcpCheckPingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigTcpCheckPingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8849ba7c7bdb2e323c625e40f813bb4da0f6e4d9c8c600a81d9031d1be44bb60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="pingsCountInput")
    def pings_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pingsCountInput"))

    @builtins.property
    @jsii.member(jsii_name="pingsCount")
    def pings_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pingsCount"))

    @pings_count.setter
    def pings_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c57ff394d61e4b461142e83117a85b0074e7fc109d186071322f7f9bed9382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pingsCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringUptimeCheckConfigTcpCheckPingConfig]:
        return typing.cast(typing.Optional[MonitoringUptimeCheckConfigTcpCheckPingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringUptimeCheckConfigTcpCheckPingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e3f8ef2c793dc11042df1322f95ded7984cc9f22a51f4cee1a7588c3dc7536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class MonitoringUptimeCheckConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#create MonitoringUptimeCheckConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#delete MonitoringUptimeCheckConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#update MonitoringUptimeCheckConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__908e637595d13c3c72cf382db55446975942b9ed52ebed29660ee5bde31a67bf)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#create MonitoringUptimeCheckConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#delete MonitoringUptimeCheckConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/monitoring_uptime_check_config#update MonitoringUptimeCheckConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringUptimeCheckConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringUptimeCheckConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringUptimeCheckConfig.MonitoringUptimeCheckConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd3d99c1286da85f4a317e4278d3cda3dee6a9da26037286279b4b73f99d0f84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2db98f579b3b6874c673f5a4b969f3e21e04303d941bc117099bae06f46d5be7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a26f06eb9a2c99f0737db3dc566fafe3fd8d74f4bcb2b5144571284300257ef1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0677ce2650aca52703589ef3a2536b8a8666adc3f47c87b1439a76641b034c3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringUptimeCheckConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringUptimeCheckConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringUptimeCheckConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d13b653febd401908b9c6e697de1ebab28ac36b4ccc86f4b2d199c9d2f2390c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MonitoringUptimeCheckConfig",
    "MonitoringUptimeCheckConfigConfig",
    "MonitoringUptimeCheckConfigContentMatchers",
    "MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher",
    "MonitoringUptimeCheckConfigContentMatchersJsonPathMatcherOutputReference",
    "MonitoringUptimeCheckConfigContentMatchersList",
    "MonitoringUptimeCheckConfigContentMatchersOutputReference",
    "MonitoringUptimeCheckConfigHttpCheck",
    "MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes",
    "MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodesList",
    "MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodesOutputReference",
    "MonitoringUptimeCheckConfigHttpCheckAuthInfo",
    "MonitoringUptimeCheckConfigHttpCheckAuthInfoOutputReference",
    "MonitoringUptimeCheckConfigHttpCheckOutputReference",
    "MonitoringUptimeCheckConfigHttpCheckPingConfig",
    "MonitoringUptimeCheckConfigHttpCheckPingConfigOutputReference",
    "MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication",
    "MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthenticationOutputReference",
    "MonitoringUptimeCheckConfigMonitoredResource",
    "MonitoringUptimeCheckConfigMonitoredResourceOutputReference",
    "MonitoringUptimeCheckConfigResourceGroup",
    "MonitoringUptimeCheckConfigResourceGroupOutputReference",
    "MonitoringUptimeCheckConfigSyntheticMonitor",
    "MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2",
    "MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2OutputReference",
    "MonitoringUptimeCheckConfigSyntheticMonitorOutputReference",
    "MonitoringUptimeCheckConfigTcpCheck",
    "MonitoringUptimeCheckConfigTcpCheckOutputReference",
    "MonitoringUptimeCheckConfigTcpCheckPingConfig",
    "MonitoringUptimeCheckConfigTcpCheckPingConfigOutputReference",
    "MonitoringUptimeCheckConfigTimeouts",
    "MonitoringUptimeCheckConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__22d6bb0db76f3b6481cdacd8b2baaec0caa6d3c2d348efdb43c628bc57f10ef0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    timeout: builtins.str,
    checker_type: typing.Optional[builtins.str] = None,
    content_matchers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringUptimeCheckConfigContentMatchers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http_check: typing.Optional[typing.Union[MonitoringUptimeCheckConfigHttpCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_check_failures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monitored_resource: typing.Optional[typing.Union[MonitoringUptimeCheckConfigMonitoredResource, typing.Dict[builtins.str, typing.Any]]] = None,
    period: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    resource_group: typing.Optional[typing.Union[MonitoringUptimeCheckConfigResourceGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    selected_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    synthetic_monitor: typing.Optional[typing.Union[MonitoringUptimeCheckConfigSyntheticMonitor, typing.Dict[builtins.str, typing.Any]]] = None,
    tcp_check: typing.Optional[typing.Union[MonitoringUptimeCheckConfigTcpCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[MonitoringUptimeCheckConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__96303b91ade2ba912ca8c62f34104bfffcd0926fff5bfbdd5241210c206ffe86(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308c164f5f07c3e529180e0b8d8424c8d85211d088b093902c0b8ec09cb442cc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringUptimeCheckConfigContentMatchers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d7bb81752ed283bb97e29bf219f2c25e3d31c7549d2703d6553b046ff394b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f4053d6cfe86fb27c9afe89d35f4d21ebefa9b145e9db253435a2542e515d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1f17ade259a632ca9baf1645b6ec1a160a8f8d6816b6cfd6ae694a26df1a64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9684dde6feac9b235757664ae06e118e045b797a4ba37e99af377c3bfaf7911a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf91fe23d8566c23e763cec977b5bb60c8bb4af33373f781464b2bffcaa1efd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58ff0c0c8e932ad95e1a4ced6a4b01ba8dd6dc00a0e01a8ac0c1578b54d6bf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e496c8345e40f328e9bb649ac59e6b31afd5c0b73e6e929cd0ec6335adf2d8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7964e1fd7fb9e7b9293e2fbcaa2b050d87d9c4d7865972768866785bfc502af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a98840566b347c2d1c2a6ac3ea29d91e6f9715ed2d128bba5464b62031f3c83(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aebab24830f7cc6e4b2db4f76a5d92a81080265c7fd9b669e2761ca3a023aa8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    timeout: builtins.str,
    checker_type: typing.Optional[builtins.str] = None,
    content_matchers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringUptimeCheckConfigContentMatchers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http_check: typing.Optional[typing.Union[MonitoringUptimeCheckConfigHttpCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_check_failures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monitored_resource: typing.Optional[typing.Union[MonitoringUptimeCheckConfigMonitoredResource, typing.Dict[builtins.str, typing.Any]]] = None,
    period: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    resource_group: typing.Optional[typing.Union[MonitoringUptimeCheckConfigResourceGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    selected_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    synthetic_monitor: typing.Optional[typing.Union[MonitoringUptimeCheckConfigSyntheticMonitor, typing.Dict[builtins.str, typing.Any]]] = None,
    tcp_check: typing.Optional[typing.Union[MonitoringUptimeCheckConfigTcpCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[MonitoringUptimeCheckConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5d5e0a38ade1b82de9c3706de1ae3020b0e5499d9f72019af7e63bba3c8a326(
    *,
    content: builtins.str,
    json_path_matcher: typing.Optional[typing.Union[MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher, typing.Dict[builtins.str, typing.Any]]] = None,
    matcher: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7831f52ff5c5afa8731494eb9e0ef121dc3d5db81b51532233bb60730525ac9d(
    *,
    json_path: builtins.str,
    json_matcher: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813376971524d5aece7a6e902b6e65b5fd5e44dce60e85c8ddde9464c4356089(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81355154d3c1adec0ad5e9279804f73b1e9e71b154f2a200f60bc96f94628ecf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff442beff99e5222c36b95b52533d36609d610d17a99ced29e2d261f35434c96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0ba523ddfdf4db5d7c4e612903c9b2ccf5d843afc9c6022aa901ea2ffd0457(
    value: typing.Optional[MonitoringUptimeCheckConfigContentMatchersJsonPathMatcher],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da637ea9032037e38a62e5394942b0c2ab26485c2b8bbbb89212cf4a75a8415(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49c8a37797472131d8d072d41f70bec6c2d3ae043d18529e630f36f0e4df553(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853513f8ee46a040c493eabb55347796b72b0d84f67319d2901b52849c148112(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f4dcea86a3e95c4f0d9dae98ced2a579f99be193f1a5ce37c05c4c55068aec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df91784e4cc57262aecbad54489961dc7eae59ecbbbd2acca8d9c29c66123d3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09701864643cd1d2e3c7de07cc835749463ca88ed5a6c60a11ab58a26c4cf340(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringUptimeCheckConfigContentMatchers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be0ba04bfd1e2a4f7a74d983a3a270203e0eec4c1fad9b82710f243cc5071036(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43dd6a401f0862f4b44c7628bde604befa7536df33c2f6213500da8aed848d75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48bd321d82885c9e23798cf1fc60210d245f07a1286a4daf3a129f7c264b2aff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c343ad10f66d852dc0b9c839c8d3a891f49d17cd53372d37eaa85b39c64ab8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringUptimeCheckConfigContentMatchers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa000a907aed1339d07ed4f8726f16ed6f3f9cb9e0f3a33740d23c3baed5a01(
    *,
    accepted_response_status_codes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_info: typing.Optional[typing.Union[MonitoringUptimeCheckConfigHttpCheckAuthInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    body: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
    custom_content_type: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mask_headers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    path: typing.Optional[builtins.str] = None,
    ping_config: typing.Optional[typing.Union[MonitoringUptimeCheckConfigHttpCheckPingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    request_method: typing.Optional[builtins.str] = None,
    service_agent_authentication: typing.Optional[typing.Union[MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    use_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    validate_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4865d480af3b8d146894971da216ed8dd30d65bd11d31c9281b084cabe5a144(
    *,
    status_class: typing.Optional[builtins.str] = None,
    status_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d56f5962b23dc713f0ffa75909b84c3c27ca36b276645af3825ec397d6c3ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0dba9f7d78303d051e0cf071bcdae54fb567f6fc292010e10bfed0320ec1868(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813a610fb8d07aeda6a6857c3427d61840c50fac217bb9bcca625e60d57e9b67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b061d6c28f7ef564382e03d5663c41ab37692e7baf72ed6654157e1f83cabe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4925490417d772c9c004f1a3dffb900d83a52bf4cef790281d70f4b35bdba0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a3b2b62e0947bf5e9ef13c6384af176453eb2138943ab81b86a3008ad3cef6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1082bf5437143b8d7ed3d6b0dce78bf9a4a32d728c16908b6d7cd19d68197c87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df7e557e4c503a29081c1fb7e4e56b315f743c591de5ea155437f7c85d67045(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a276ffd2a41cea8612210dad752d57e8005c20cf7995282f29c9c556fd578912(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae7ddb80723d9da12276766927d24ea8dc3d3c0e5e29ba6c1b55dee366f4d568(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b002f871fd2676a9251fc5e0d16bf6af6fc5d857a07a5252ace1d680d6768d0(
    *,
    username: builtins.str,
    password: typing.Optional[builtins.str] = None,
    password_wo: typing.Optional[builtins.str] = None,
    password_wo_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e76bfcd9df7a2e362fd69bd7db677cccc6dedd18ea10fdc2b2cf9d55856458(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c63901d2e3a2e4e59c1867e911089dda5353f6804ec1814fce15440bf37948e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5bd482f3c39109f63aeec446f2248b7611507faeb0af2ee6285ceda7a9bbcc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c09e56737505038801027505774a4d7aaa3a1acc5af112cb534b62ceb2c31a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894134ddcf72e731262d775bd895cf6fc600371bedddd79b2219b75d0284592a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077f182a7be5152b622bb7d649f7e7cd7d433bd5f175533abc390c8b2b0b337e(
    value: typing.Optional[MonitoringUptimeCheckConfigHttpCheckAuthInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c21a00172d3ee361100efa5506a3b7565ed34f6004c4f692e220341977e16a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff28f71fb3aefeef9815aa4b6ebd3184e10850b32248eff242102275b35145c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringUptimeCheckConfigHttpCheckAcceptedResponseStatusCodes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40676f8cc05dd594dca2fba8a0a5fb5fcd8dae1d62bd2fba43f98976fc54e9b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021b232f7b07e98b9df8c9feaf3dd7d60569490ee7bbb44ce3d6835b9c49af9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99dfa8cc51520859ad7afc8719acdc48c7223523aa83c2d75d4c435394b63eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1033c129ad7a29ab4d95a6f285d1b75f9f0841b507d16636f0cd152ce3adda(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2f5eb2045b8b1be108160fdcf224a6240a0dc3677ea875d468fee831e565d4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b50bdc7807579cb466679f1a1ff8c87d024c25138685be32287e74cfba8e70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ba4dcecf05b1a5c046729882b73554f1a01039e1cd4c0b152fdfcbdc9c1c0f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e2d5a3200d25e54e5fab6e269b346df50b16d78c675ab67841d8f9642e67c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9a641833fc63dec5771d9c0fcb49a4963de009c80041fad59abce4eab713f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da645f5fbeea09606bd68b62e432dbec87853c7e0c990b0473d708901769ef4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f259a1cae23cb893e2316de7fbd5803aee1e3e8916bb248621985a2a5e9a3af(
    value: typing.Optional[MonitoringUptimeCheckConfigHttpCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9393784c6207b165f26d296ca9ca60877d5017cb7ded18ab7759f86bea6d75(
    *,
    pings_count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a51d967d069ca7df14d2b17aee677e1e2db9d6ae5d2162d142c48169529c0f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08fcb22f63194a27ac581e758cbb09d2bfb57ef12283b9e7513411ca5e3ce927(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa045d073e77b8db4088ff4cfa787923bddd718fc2995bba4f1915301a083ff(
    value: typing.Optional[MonitoringUptimeCheckConfigHttpCheckPingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797e498aa4f065f2c8b66236b8dc9b4d81d1efc1bf316219c014b20a0bf58b04(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a810b52496d66a9b0d232b5827710a51eaba51328c73482fc19caea69356b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7036d6dbe1fb50cc8a23c8c380391d458771b62b1368c970ae2588b413ed63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2a7d816997b2f64a3ad7c95d0f637668c5478f87a78632e6b1477b520ac397(
    value: typing.Optional[MonitoringUptimeCheckConfigHttpCheckServiceAgentAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a57ea68e8381a7e5d16034ebd9450191978ee55104d6ab243d0fe1c31124e4(
    *,
    labels: typing.Mapping[builtins.str, builtins.str],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05cc776cfb5087225b2e75dc323c995323cf82789df54b7c715fa8f8222ee5f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d9b458d405fd37abb15e4fdd28cb39090e009870269a476cf1de26f82556df(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea5e5d1aa63996d8e60ca7be5ee49bc5560f9d41150c3e11b4d851901cc81613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e6fbb2efce74b900163b90305e58f0a5c42691a50bfea7de3ad857a4793b20(
    value: typing.Optional[MonitoringUptimeCheckConfigMonitoredResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f100667c91205d0928732278ba1d7ec789499ca2bd0e0153ade457ef0fe77af9(
    *,
    group_id: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b1563b42eafc1c052514046b1dc96b9a4bc5b957ccb08d7c0b026dc6efddc2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43eac06ee4ec61dd5b12d9f04fc5c22538992db5e0ec3839ed95573d0982e586(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8af517224eb9d280c9724755e95c24e57eba1c5b6d49a5d9539405547dd2e7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a834491cb0b97707e80f95aeef79adb46a123b041f1517112a3a47481c0a5642(
    value: typing.Optional[MonitoringUptimeCheckConfigResourceGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a024a5207279280261ed4d86546b9af6c81f1f271f2d2de25ff7f3c83a8887(
    *,
    cloud_function_v2: typing.Union[MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92fc8a68cedf84bacf306212f95787a8142dbecaf60ee508e168b159a9bca9d9(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f784ed1c14559b6d9a65d0f742d8ee3b9e5b3baba193c43281d31208b2bebb84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea5b8df51c29c2abf5e0c6cc392fe3e781cde2d7b6e81a07d66940be50d0fd26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88acaa2852f0e9d2050dbfba811ab92da10bcadbbf2199e2e45490418eb9559b(
    value: typing.Optional[MonitoringUptimeCheckConfigSyntheticMonitorCloudFunctionV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b3d488661b61e9572a718f7c8dd7103071fa12d7f962ae90fbc66e20a23ac3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0075fbcde952498715f53aa3e177dcaf0a68423017ac8f5118cb51d97aed2c(
    value: typing.Optional[MonitoringUptimeCheckConfigSyntheticMonitor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aefdc46fd2e3e339e665901fa9ab5c8ca8d4abd40fdc618af240bc0665d5aacd(
    *,
    port: jsii.Number,
    ping_config: typing.Optional[typing.Union[MonitoringUptimeCheckConfigTcpCheckPingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7cab9781a672bc648150addc0cbc0fa7dd5cd09914adf936d58ee77bbef1b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dcbb07332e613233b2285b4b635cbdf344e427b472aeb6e893d71bf8136f3d0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ab91a68b8012fe5e2be726ccc3014139b4567f2f4c2230c182932cf4989a82(
    value: typing.Optional[MonitoringUptimeCheckConfigTcpCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95fcdaaa5003ffe6495da67d1384d1c57c1302fad80d128677cf37fb50241a06(
    *,
    pings_count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8849ba7c7bdb2e323c625e40f813bb4da0f6e4d9c8c600a81d9031d1be44bb60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c57ff394d61e4b461142e83117a85b0074e7fc109d186071322f7f9bed9382(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e3f8ef2c793dc11042df1322f95ded7984cc9f22a51f4cee1a7588c3dc7536(
    value: typing.Optional[MonitoringUptimeCheckConfigTcpCheckPingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908e637595d13c3c72cf382db55446975942b9ed52ebed29660ee5bde31a67bf(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd3d99c1286da85f4a317e4278d3cda3dee6a9da26037286279b4b73f99d0f84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db98f579b3b6874c673f5a4b969f3e21e04303d941bc117099bae06f46d5be7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26f06eb9a2c99f0737db3dc566fafe3fd8d74f4bcb2b5144571284300257ef1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0677ce2650aca52703589ef3a2536b8a8666adc3f47c87b1439a76641b034c3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d13b653febd401908b9c6e697de1ebab28ac36b4ccc86f4b2d199c9d2f2390c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitoringUptimeCheckConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
