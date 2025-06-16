r'''
# `google_network_services_edge_cache_origin`

Refer to the Terraform Registry for docs: [`google_network_services_edge_cache_origin`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin).
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


class GoogleNetworkServicesEdgeCacheOrigin(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOrigin",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin google_network_services_edge_cache_origin}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        origin_address: builtins.str,
        aws_v4_authentication: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        failover_origin: typing.Optional[builtins.str] = None,
        flex_shielding: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheOriginFlexShielding", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_attempts: typing.Optional[jsii.Number] = None,
        origin_override_action: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction", typing.Dict[builtins.str, typing.Any]]] = None,
        origin_redirect: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheOriginOriginRedirect", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheOriginTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheOriginTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin google_network_services_edge_cache_origin} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#name GoogleNetworkServicesEdgeCacheOrigin#name}
        :param origin_address: A fully qualified domain name (FQDN) or IP address reachable over the public Internet, or the address of a Google Cloud Storage bucket. This address will be used as the origin for cache requests - e.g. FQDN: media-backend.example.com, IPv4: 35.218.1.1, IPv6: 2607:f8b0:4012:809::200e, Cloud Storage: gs://bucketname When providing an FQDN (hostname), it must be publicly resolvable (e.g. via Google public DNS) and IP addresses must be publicly routable. It must not contain a protocol (e.g., https://) and it must not contain any slashes. If a Cloud Storage bucket is provided, it must be in the canonical "gs://bucketname" format. Other forms, such as "storage.googleapis.com", will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#origin_address GoogleNetworkServicesEdgeCacheOrigin#origin_address}
        :param aws_v4_authentication: aws_v4_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#aws_v4_authentication GoogleNetworkServicesEdgeCacheOrigin#aws_v4_authentication}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#description GoogleNetworkServicesEdgeCacheOrigin#description}
        :param failover_origin: The Origin resource to try when the current origin cannot be reached. After maxAttempts is reached, the configured failoverOrigin will be used to fulfil the request. The value of timeout.maxAttemptsTimeout dictates the timeout across all origins. A reference to a Topic resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#failover_origin GoogleNetworkServicesEdgeCacheOrigin#failover_origin}
        :param flex_shielding: flex_shielding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#flex_shielding GoogleNetworkServicesEdgeCacheOrigin#flex_shielding}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#id GoogleNetworkServicesEdgeCacheOrigin#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the EdgeCache resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#labels GoogleNetworkServicesEdgeCacheOrigin#labels}
        :param max_attempts: The maximum number of attempts to cache fill from this origin. Another attempt is made when a cache fill fails with one of the retryConditions. Once maxAttempts to this origin have failed the failoverOrigin will be used, if one is specified. That failoverOrigin may specify its own maxAttempts, retryConditions and failoverOrigin to control its own cache fill failures. The total number of allowed attempts to cache fill across this and failover origins is limited to four. The total time allowed for cache fill attempts across this and failover origins can be controlled with maxAttemptsTimeout. The last valid, non-retried response from all origins will be returned to the client. If no origin returns a valid response, an HTTP 502 will be returned to the client. Defaults to 1. Must be a value greater than 0 and less than 4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#max_attempts GoogleNetworkServicesEdgeCacheOrigin#max_attempts}
        :param origin_override_action: origin_override_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#origin_override_action GoogleNetworkServicesEdgeCacheOrigin#origin_override_action}
        :param origin_redirect: origin_redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#origin_redirect GoogleNetworkServicesEdgeCacheOrigin#origin_redirect}
        :param port: The port to connect to the origin on. Defaults to port 443 for HTTP2 and HTTPS protocols, and port 80 for HTTP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#port GoogleNetworkServicesEdgeCacheOrigin#port}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#project GoogleNetworkServicesEdgeCacheOrigin#project}.
        :param protocol: The protocol to use to connect to the configured origin. Defaults to HTTP2, and it is strongly recommended that users use HTTP2 for both security & performance. When using HTTP2 or HTTPS as the protocol, a valid, publicly-signed, unexpired TLS (SSL) certificate must be presented by the origin server. Possible values: ["HTTP2", "HTTPS", "HTTP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#protocol GoogleNetworkServicesEdgeCacheOrigin#protocol}
        :param retry_conditions: Specifies one or more retry conditions for the configured origin. If the failure mode during a connection attempt to the origin matches the configured retryCondition(s), the origin request will be retried up to maxAttempts times. The failoverOrigin, if configured, will then be used to satisfy the request. The default retryCondition is "CONNECT_FAILURE". retryConditions apply to this origin, and not subsequent failoverOrigin(s), which may specify their own retryConditions and maxAttempts. Valid values are: - CONNECT_FAILURE: Retry on failures connecting to origins, for example due to connection timeouts. - HTTP_5XX: Retry if the origin responds with any 5xx response code, or if the origin does not respond at all, example: disconnects, reset, read timeout, connection failure, and refused streams. - GATEWAY_ERROR: Similar to 5xx, but only applies to response codes 502, 503 or 504. - RETRIABLE_4XX: Retry for retriable 4xx response codes, which include HTTP 409 (Conflict) and HTTP 429 (Too Many Requests) - NOT_FOUND: Retry if the origin returns a HTTP 404 (Not Found). This can be useful when generating video content, and the segment is not available yet. - FORBIDDEN: Retry if the origin returns a HTTP 403 (Forbidden). Possible values: ["CONNECT_FAILURE", "HTTP_5XX", "GATEWAY_ERROR", "RETRIABLE_4XX", "NOT_FOUND", "FORBIDDEN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#retry_conditions GoogleNetworkServicesEdgeCacheOrigin#retry_conditions}
        :param timeout: timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#timeout GoogleNetworkServicesEdgeCacheOrigin#timeout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#timeouts GoogleNetworkServicesEdgeCacheOrigin#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6edf6d811003f0d49b47da92d641f38476538f976897594107c7af11fd124bc5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleNetworkServicesEdgeCacheOriginConfig(
            name=name,
            origin_address=origin_address,
            aws_v4_authentication=aws_v4_authentication,
            description=description,
            failover_origin=failover_origin,
            flex_shielding=flex_shielding,
            id=id,
            labels=labels,
            max_attempts=max_attempts,
            origin_override_action=origin_override_action,
            origin_redirect=origin_redirect,
            port=port,
            project=project,
            protocol=protocol,
            retry_conditions=retry_conditions,
            timeout=timeout,
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
        '''Generates CDKTF code for importing a GoogleNetworkServicesEdgeCacheOrigin resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleNetworkServicesEdgeCacheOrigin to import.
        :param import_from_id: The id of the existing GoogleNetworkServicesEdgeCacheOrigin that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleNetworkServicesEdgeCacheOrigin to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12548fec5e913d72d6205ebdc945d2bf28f9211cf65ce0aff707f15276880740)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAwsV4Authentication")
    def put_aws_v4_authentication(
        self,
        *,
        access_key_id: builtins.str,
        origin_region: builtins.str,
        secret_access_key_version: builtins.str,
    ) -> None:
        '''
        :param access_key_id: The access key ID your origin uses to identify the key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#access_key_id GoogleNetworkServicesEdgeCacheOrigin#access_key_id}
        :param origin_region: The name of the AWS region that your origin is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#origin_region GoogleNetworkServicesEdgeCacheOrigin#origin_region}
        :param secret_access_key_version: The Secret Manager secret version of the secret access key used by your origin. This is the resource name of the secret version in the format 'projects/* /secrets/* /versions/*' where the '*' values are replaced by the project, secret, and version you require. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#secret_access_key_version GoogleNetworkServicesEdgeCacheOrigin#secret_access_key_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication(
            access_key_id=access_key_id,
            origin_region=origin_region,
            secret_access_key_version=secret_access_key_version,
        )

        return typing.cast(None, jsii.invoke(self, "putAwsV4Authentication", [value]))

    @jsii.member(jsii_name="putFlexShielding")
    def put_flex_shielding(
        self,
        *,
        flex_shielding_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param flex_shielding_regions: Whenever possible, content will be fetched from origin and cached in or near the specified origin. Best effort. You must specify exactly one FlexShieldingRegion. Possible values: ["AFRICA_SOUTH1", "ME_CENTRAL1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#flex_shielding_regions GoogleNetworkServicesEdgeCacheOrigin#flex_shielding_regions}
        '''
        value = GoogleNetworkServicesEdgeCacheOriginFlexShielding(
            flex_shielding_regions=flex_shielding_regions
        )

        return typing.cast(None, jsii.invoke(self, "putFlexShielding", [value]))

    @jsii.member(jsii_name="putOriginOverrideAction")
    def put_origin_override_action(
        self,
        *,
        header_action: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction", typing.Dict[builtins.str, typing.Any]]] = None,
        url_rewrite: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param header_action: header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#header_action GoogleNetworkServicesEdgeCacheOrigin#header_action}
        :param url_rewrite: url_rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#url_rewrite GoogleNetworkServicesEdgeCacheOrigin#url_rewrite}
        '''
        value = GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction(
            header_action=header_action, url_rewrite=url_rewrite
        )

        return typing.cast(None, jsii.invoke(self, "putOriginOverrideAction", [value]))

    @jsii.member(jsii_name="putOriginRedirect")
    def put_origin_redirect(
        self,
        *,
        redirect_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param redirect_conditions: The set of redirect response codes that the CDN follows. Values of `RedirectConditions <https://cloud.google.com/media-cdn/docs/reference/rest/v1/projects.locations.edgeCacheOrigins#redirectconditions>`_ are accepted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#redirect_conditions GoogleNetworkServicesEdgeCacheOrigin#redirect_conditions}
        '''
        value = GoogleNetworkServicesEdgeCacheOriginOriginRedirect(
            redirect_conditions=redirect_conditions
        )

        return typing.cast(None, jsii.invoke(self, "putOriginRedirect", [value]))

    @jsii.member(jsii_name="putTimeout")
    def put_timeout(
        self,
        *,
        connect_timeout: typing.Optional[builtins.str] = None,
        max_attempts_timeout: typing.Optional[builtins.str] = None,
        read_timeout: typing.Optional[builtins.str] = None,
        response_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connect_timeout: The maximum duration to wait for a single origin connection to be established, including DNS lookup, TLS handshake and TCP/QUIC connection establishment. Defaults to 5 seconds. The timeout must be a value between 1s and 15s. The connectTimeout capped by the deadline set by the request's maxAttemptsTimeout. The last connection attempt may have a smaller connectTimeout in order to adhere to the overall maxAttemptsTimeout. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#connect_timeout GoogleNetworkServicesEdgeCacheOrigin#connect_timeout}
        :param max_attempts_timeout: The maximum time across all connection attempts to the origin, including failover origins, before returning an error to the client. A HTTP 504 will be returned if the timeout is reached before a response is returned. Defaults to 15 seconds. The timeout must be a value between 1s and 30s. If a failoverOrigin is specified, the maxAttemptsTimeout of the first configured origin sets the deadline for all connection attempts across all failoverOrigins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#max_attempts_timeout GoogleNetworkServicesEdgeCacheOrigin#max_attempts_timeout}
        :param read_timeout: The maximum duration to wait between reads of a single HTTP connection/stream. Defaults to 15 seconds. The timeout must be a value between 1s and 30s. The readTimeout is capped by the responseTimeout. All reads of the HTTP connection/stream must be completed by the deadline set by the responseTimeout. If the response headers have already been written to the connection, the response will be truncated and logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#read_timeout GoogleNetworkServicesEdgeCacheOrigin#read_timeout}
        :param response_timeout: The maximum duration to wait for the last byte of a response to arrive when reading from the HTTP connection/stream. Defaults to 30 seconds. The timeout must be a value between 1s and 120s. The responseTimeout starts after the connection has been established. This also applies to HTTP Chunked Transfer Encoding responses, and/or when an open-ended Range request is made to the origin. Origins that take longer to write additional bytes to the response than the configured responseTimeout will result in an error being returned to the client. If the response headers have already been written to the connection, the response will be truncated and logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#response_timeout GoogleNetworkServicesEdgeCacheOrigin#response_timeout}
        '''
        value = GoogleNetworkServicesEdgeCacheOriginTimeout(
            connect_timeout=connect_timeout,
            max_attempts_timeout=max_attempts_timeout,
            read_timeout=read_timeout,
            response_timeout=response_timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putTimeout", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#create GoogleNetworkServicesEdgeCacheOrigin#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#delete GoogleNetworkServicesEdgeCacheOrigin#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#update GoogleNetworkServicesEdgeCacheOrigin#update}.
        '''
        value = GoogleNetworkServicesEdgeCacheOriginTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAwsV4Authentication")
    def reset_aws_v4_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsV4Authentication", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFailoverOrigin")
    def reset_failover_origin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailoverOrigin", []))

    @jsii.member(jsii_name="resetFlexShielding")
    def reset_flex_shielding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlexShielding", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMaxAttempts")
    def reset_max_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAttempts", []))

    @jsii.member(jsii_name="resetOriginOverrideAction")
    def reset_origin_override_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginOverrideAction", []))

    @jsii.member(jsii_name="resetOriginRedirect")
    def reset_origin_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginRedirect", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetRetryConditions")
    def reset_retry_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryConditions", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

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
    @jsii.member(jsii_name="awsV4Authentication")
    def aws_v4_authentication(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheOriginAwsV4AuthenticationOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheOriginAwsV4AuthenticationOutputReference", jsii.get(self, "awsV4Authentication"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="flexShielding")
    def flex_shielding(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheOriginFlexShieldingOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheOriginFlexShieldingOutputReference", jsii.get(self, "flexShielding"))

    @builtins.property
    @jsii.member(jsii_name="originOverrideAction")
    def origin_override_action(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionOutputReference", jsii.get(self, "originOverrideAction"))

    @builtins.property
    @jsii.member(jsii_name="originRedirect")
    def origin_redirect(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheOriginOriginRedirectOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheOriginOriginRedirectOutputReference", jsii.get(self, "originRedirect"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> "GoogleNetworkServicesEdgeCacheOriginTimeoutOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheOriginTimeoutOutputReference", jsii.get(self, "timeout"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleNetworkServicesEdgeCacheOriginTimeoutsOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheOriginTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="awsV4AuthenticationInput")
    def aws_v4_authentication_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication"], jsii.get(self, "awsV4AuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverOriginInput")
    def failover_origin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "failoverOriginInput"))

    @builtins.property
    @jsii.member(jsii_name="flexShieldingInput")
    def flex_shielding_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheOriginFlexShielding"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheOriginFlexShielding"], jsii.get(self, "flexShieldingInput"))

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
    @jsii.member(jsii_name="maxAttemptsInput")
    def max_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="originAddressInput")
    def origin_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="originOverrideActionInput")
    def origin_override_action_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction"], jsii.get(self, "originOverrideActionInput"))

    @builtins.property
    @jsii.member(jsii_name="originRedirectInput")
    def origin_redirect_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheOriginOriginRedirect"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheOriginOriginRedirect"], jsii.get(self, "originRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="retryConditionsInput")
    def retry_conditions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "retryConditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheOriginTimeout"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheOriginTimeout"], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkServicesEdgeCacheOriginTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkServicesEdgeCacheOriginTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39bdee2717886a78ea10ed0bfe88a615b1d255ca1a92e9e574c89906bef1f07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failoverOrigin")
    def failover_origin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failoverOrigin"))

    @failover_origin.setter
    def failover_origin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5d09a38137560a2e9788df7aa56fc28afc056bc6837de6f889b233ae29bc78a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverOrigin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c474d60b4882a22782e41845e494f55ed8389165e805a251aec82b18fae792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e5b76fe9f9639351030e98e70e93c23eb8cc68067fe387933252fb722ec83c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAttempts")
    def max_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAttempts"))

    @max_attempts.setter
    def max_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c4841fab67b7bc8a526001d38dabf2d40496af58540f39ab8d7978162d33a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f952c7027c8b10d79fc19ecbf5acdd8c62062637d87e985a0a793807133b77b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originAddress")
    def origin_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originAddress"))

    @origin_address.setter
    def origin_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42cf73349191780bbdfa2fc083155fbe1cd37e2a672ebd50408212ccf7cedb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5da9109b4ee2e1d0b1adc67da5fb0e068e79cefbcd560605b56f486e04464b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d09230361e43a53221a7af8ea498cec2bb910a6e397dd13efaa0215ca56caf91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddfae4d7d6b6263408f7d28d92094ee538d7894b0c10310eed1c84d1d604ab6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryConditions")
    def retry_conditions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "retryConditions"))

    @retry_conditions.setter
    def retry_conditions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92eeb0d206432d00377ce1eac8c73f7c90245266d6d71e6f576190a5dce00c7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryConditions", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id": "accessKeyId",
        "origin_region": "originRegion",
        "secret_access_key_version": "secretAccessKeyVersion",
    },
)
class GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication:
    def __init__(
        self,
        *,
        access_key_id: builtins.str,
        origin_region: builtins.str,
        secret_access_key_version: builtins.str,
    ) -> None:
        '''
        :param access_key_id: The access key ID your origin uses to identify the key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#access_key_id GoogleNetworkServicesEdgeCacheOrigin#access_key_id}
        :param origin_region: The name of the AWS region that your origin is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#origin_region GoogleNetworkServicesEdgeCacheOrigin#origin_region}
        :param secret_access_key_version: The Secret Manager secret version of the secret access key used by your origin. This is the resource name of the secret version in the format 'projects/* /secrets/* /versions/*' where the '*' values are replaced by the project, secret, and version you require. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#secret_access_key_version GoogleNetworkServicesEdgeCacheOrigin#secret_access_key_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d37da7508515c5002e8db578e2074d88f098a82e2f885f6627f1e4cd2f31fa42)
            check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
            check_type(argname="argument origin_region", value=origin_region, expected_type=type_hints["origin_region"])
            check_type(argname="argument secret_access_key_version", value=secret_access_key_version, expected_type=type_hints["secret_access_key_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_key_id": access_key_id,
            "origin_region": origin_region,
            "secret_access_key_version": secret_access_key_version,
        }

    @builtins.property
    def access_key_id(self) -> builtins.str:
        '''The access key ID your origin uses to identify the key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#access_key_id GoogleNetworkServicesEdgeCacheOrigin#access_key_id}
        '''
        result = self._values.get("access_key_id")
        assert result is not None, "Required property 'access_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin_region(self) -> builtins.str:
        '''The name of the AWS region that your origin is in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#origin_region GoogleNetworkServicesEdgeCacheOrigin#origin_region}
        '''
        result = self._values.get("origin_region")
        assert result is not None, "Required property 'origin_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_access_key_version(self) -> builtins.str:
        '''The Secret Manager secret version of the secret access key used by your origin.

        This is the resource name of the secret version in the format 'projects/* /secrets/* /versions/*' where the '*' values are replaced by the project, secret, and version you require.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#secret_access_key_version GoogleNetworkServicesEdgeCacheOrigin#secret_access_key_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("secret_access_key_version")
        assert result is not None, "Required property 'secret_access_key_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheOriginAwsV4AuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginAwsV4AuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90dec2c7153ea3e3a1ecb457aef42f642d1907a637ba926d98841e8c085b509d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="accessKeyIdInput")
    def access_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="originRegionInput")
    def origin_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyVersionInput")
    def secret_access_key_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretAccessKeyVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKeyId"))

    @access_key_id.setter
    def access_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34828e6d5247679ec270cfe738666945f1e1b19e1a70c98d6191b7d4f50bbf32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originRegion")
    def origin_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originRegion"))

    @origin_region.setter
    def origin_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86fc984fdaf02eb9bc05f218cc080d33e1c946b9f12aade064edbd1e9433d5bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyVersion")
    def secret_access_key_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretAccessKeyVersion"))

    @secret_access_key_version.setter
    def secret_access_key_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0f2f0ec64ce57827efb93376bb690801b2830e117108023c0e959cc88f54710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKeyVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fef23eb20fc90b564a990302ecb2e7978dbf760f85c405b8e195a9e05233b9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginConfig",
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
        "origin_address": "originAddress",
        "aws_v4_authentication": "awsV4Authentication",
        "description": "description",
        "failover_origin": "failoverOrigin",
        "flex_shielding": "flexShielding",
        "id": "id",
        "labels": "labels",
        "max_attempts": "maxAttempts",
        "origin_override_action": "originOverrideAction",
        "origin_redirect": "originRedirect",
        "port": "port",
        "project": "project",
        "protocol": "protocol",
        "retry_conditions": "retryConditions",
        "timeout": "timeout",
        "timeouts": "timeouts",
    },
)
class GoogleNetworkServicesEdgeCacheOriginConfig(
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
        origin_address: builtins.str,
        aws_v4_authentication: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        failover_origin: typing.Optional[builtins.str] = None,
        flex_shielding: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheOriginFlexShielding", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_attempts: typing.Optional[jsii.Number] = None,
        origin_override_action: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction", typing.Dict[builtins.str, typing.Any]]] = None,
        origin_redirect: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheOriginOriginRedirect", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheOriginTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheOriginTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#name GoogleNetworkServicesEdgeCacheOrigin#name}
        :param origin_address: A fully qualified domain name (FQDN) or IP address reachable over the public Internet, or the address of a Google Cloud Storage bucket. This address will be used as the origin for cache requests - e.g. FQDN: media-backend.example.com, IPv4: 35.218.1.1, IPv6: 2607:f8b0:4012:809::200e, Cloud Storage: gs://bucketname When providing an FQDN (hostname), it must be publicly resolvable (e.g. via Google public DNS) and IP addresses must be publicly routable. It must not contain a protocol (e.g., https://) and it must not contain any slashes. If a Cloud Storage bucket is provided, it must be in the canonical "gs://bucketname" format. Other forms, such as "storage.googleapis.com", will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#origin_address GoogleNetworkServicesEdgeCacheOrigin#origin_address}
        :param aws_v4_authentication: aws_v4_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#aws_v4_authentication GoogleNetworkServicesEdgeCacheOrigin#aws_v4_authentication}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#description GoogleNetworkServicesEdgeCacheOrigin#description}
        :param failover_origin: The Origin resource to try when the current origin cannot be reached. After maxAttempts is reached, the configured failoverOrigin will be used to fulfil the request. The value of timeout.maxAttemptsTimeout dictates the timeout across all origins. A reference to a Topic resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#failover_origin GoogleNetworkServicesEdgeCacheOrigin#failover_origin}
        :param flex_shielding: flex_shielding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#flex_shielding GoogleNetworkServicesEdgeCacheOrigin#flex_shielding}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#id GoogleNetworkServicesEdgeCacheOrigin#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the EdgeCache resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#labels GoogleNetworkServicesEdgeCacheOrigin#labels}
        :param max_attempts: The maximum number of attempts to cache fill from this origin. Another attempt is made when a cache fill fails with one of the retryConditions. Once maxAttempts to this origin have failed the failoverOrigin will be used, if one is specified. That failoverOrigin may specify its own maxAttempts, retryConditions and failoverOrigin to control its own cache fill failures. The total number of allowed attempts to cache fill across this and failover origins is limited to four. The total time allowed for cache fill attempts across this and failover origins can be controlled with maxAttemptsTimeout. The last valid, non-retried response from all origins will be returned to the client. If no origin returns a valid response, an HTTP 502 will be returned to the client. Defaults to 1. Must be a value greater than 0 and less than 4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#max_attempts GoogleNetworkServicesEdgeCacheOrigin#max_attempts}
        :param origin_override_action: origin_override_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#origin_override_action GoogleNetworkServicesEdgeCacheOrigin#origin_override_action}
        :param origin_redirect: origin_redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#origin_redirect GoogleNetworkServicesEdgeCacheOrigin#origin_redirect}
        :param port: The port to connect to the origin on. Defaults to port 443 for HTTP2 and HTTPS protocols, and port 80 for HTTP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#port GoogleNetworkServicesEdgeCacheOrigin#port}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#project GoogleNetworkServicesEdgeCacheOrigin#project}.
        :param protocol: The protocol to use to connect to the configured origin. Defaults to HTTP2, and it is strongly recommended that users use HTTP2 for both security & performance. When using HTTP2 or HTTPS as the protocol, a valid, publicly-signed, unexpired TLS (SSL) certificate must be presented by the origin server. Possible values: ["HTTP2", "HTTPS", "HTTP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#protocol GoogleNetworkServicesEdgeCacheOrigin#protocol}
        :param retry_conditions: Specifies one or more retry conditions for the configured origin. If the failure mode during a connection attempt to the origin matches the configured retryCondition(s), the origin request will be retried up to maxAttempts times. The failoverOrigin, if configured, will then be used to satisfy the request. The default retryCondition is "CONNECT_FAILURE". retryConditions apply to this origin, and not subsequent failoverOrigin(s), which may specify their own retryConditions and maxAttempts. Valid values are: - CONNECT_FAILURE: Retry on failures connecting to origins, for example due to connection timeouts. - HTTP_5XX: Retry if the origin responds with any 5xx response code, or if the origin does not respond at all, example: disconnects, reset, read timeout, connection failure, and refused streams. - GATEWAY_ERROR: Similar to 5xx, but only applies to response codes 502, 503 or 504. - RETRIABLE_4XX: Retry for retriable 4xx response codes, which include HTTP 409 (Conflict) and HTTP 429 (Too Many Requests) - NOT_FOUND: Retry if the origin returns a HTTP 404 (Not Found). This can be useful when generating video content, and the segment is not available yet. - FORBIDDEN: Retry if the origin returns a HTTP 403 (Forbidden). Possible values: ["CONNECT_FAILURE", "HTTP_5XX", "GATEWAY_ERROR", "RETRIABLE_4XX", "NOT_FOUND", "FORBIDDEN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#retry_conditions GoogleNetworkServicesEdgeCacheOrigin#retry_conditions}
        :param timeout: timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#timeout GoogleNetworkServicesEdgeCacheOrigin#timeout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#timeouts GoogleNetworkServicesEdgeCacheOrigin#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(aws_v4_authentication, dict):
            aws_v4_authentication = GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication(**aws_v4_authentication)
        if isinstance(flex_shielding, dict):
            flex_shielding = GoogleNetworkServicesEdgeCacheOriginFlexShielding(**flex_shielding)
        if isinstance(origin_override_action, dict):
            origin_override_action = GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction(**origin_override_action)
        if isinstance(origin_redirect, dict):
            origin_redirect = GoogleNetworkServicesEdgeCacheOriginOriginRedirect(**origin_redirect)
        if isinstance(timeout, dict):
            timeout = GoogleNetworkServicesEdgeCacheOriginTimeout(**timeout)
        if isinstance(timeouts, dict):
            timeouts = GoogleNetworkServicesEdgeCacheOriginTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2897b17b9a743f41d006328108815afbb72c2572dccbce491858f0b655dcff94)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument origin_address", value=origin_address, expected_type=type_hints["origin_address"])
            check_type(argname="argument aws_v4_authentication", value=aws_v4_authentication, expected_type=type_hints["aws_v4_authentication"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument failover_origin", value=failover_origin, expected_type=type_hints["failover_origin"])
            check_type(argname="argument flex_shielding", value=flex_shielding, expected_type=type_hints["flex_shielding"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument max_attempts", value=max_attempts, expected_type=type_hints["max_attempts"])
            check_type(argname="argument origin_override_action", value=origin_override_action, expected_type=type_hints["origin_override_action"])
            check_type(argname="argument origin_redirect", value=origin_redirect, expected_type=type_hints["origin_redirect"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument retry_conditions", value=retry_conditions, expected_type=type_hints["retry_conditions"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "origin_address": origin_address,
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
        if aws_v4_authentication is not None:
            self._values["aws_v4_authentication"] = aws_v4_authentication
        if description is not None:
            self._values["description"] = description
        if failover_origin is not None:
            self._values["failover_origin"] = failover_origin
        if flex_shielding is not None:
            self._values["flex_shielding"] = flex_shielding
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if max_attempts is not None:
            self._values["max_attempts"] = max_attempts
        if origin_override_action is not None:
            self._values["origin_override_action"] = origin_override_action
        if origin_redirect is not None:
            self._values["origin_redirect"] = origin_redirect
        if port is not None:
            self._values["port"] = port
        if project is not None:
            self._values["project"] = project
        if protocol is not None:
            self._values["protocol"] = protocol
        if retry_conditions is not None:
            self._values["retry_conditions"] = retry_conditions
        if timeout is not None:
            self._values["timeout"] = timeout
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#name GoogleNetworkServicesEdgeCacheOrigin#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin_address(self) -> builtins.str:
        '''A fully qualified domain name (FQDN) or IP address reachable over the public Internet, or the address of a Google Cloud Storage bucket.

        This address will be used as the origin for cache requests - e.g. FQDN: media-backend.example.com, IPv4: 35.218.1.1, IPv6: 2607:f8b0:4012:809::200e, Cloud Storage: gs://bucketname

        When providing an FQDN (hostname), it must be publicly resolvable (e.g. via Google public DNS) and IP addresses must be publicly routable.  It must not contain a protocol (e.g., https://) and it must not contain any slashes.
        If a Cloud Storage bucket is provided, it must be in the canonical "gs://bucketname" format. Other forms, such as "storage.googleapis.com", will be rejected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#origin_address GoogleNetworkServicesEdgeCacheOrigin#origin_address}
        '''
        result = self._values.get("origin_address")
        assert result is not None, "Required property 'origin_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_v4_authentication(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication]:
        '''aws_v4_authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#aws_v4_authentication GoogleNetworkServicesEdgeCacheOrigin#aws_v4_authentication}
        '''
        result = self._values.get("aws_v4_authentication")
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#description GoogleNetworkServicesEdgeCacheOrigin#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failover_origin(self) -> typing.Optional[builtins.str]:
        '''The Origin resource to try when the current origin cannot be reached.

        After maxAttempts is reached, the configured failoverOrigin will be used to fulfil the request.

        The value of timeout.maxAttemptsTimeout dictates the timeout across all origins.
        A reference to a Topic resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#failover_origin GoogleNetworkServicesEdgeCacheOrigin#failover_origin}
        '''
        result = self._values.get("failover_origin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flex_shielding(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheOriginFlexShielding"]:
        '''flex_shielding block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#flex_shielding GoogleNetworkServicesEdgeCacheOrigin#flex_shielding}
        '''
        result = self._values.get("flex_shielding")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheOriginFlexShielding"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#id GoogleNetworkServicesEdgeCacheOrigin#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#labels GoogleNetworkServicesEdgeCacheOrigin#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_attempts(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of attempts to cache fill from this origin.

        Another attempt is made when a cache fill fails with one of the retryConditions.

        Once maxAttempts to this origin have failed the failoverOrigin will be used, if one is specified. That failoverOrigin may specify its own maxAttempts,
        retryConditions and failoverOrigin to control its own cache fill failures.

        The total number of allowed attempts to cache fill across this and failover origins is limited to four.
        The total time allowed for cache fill attempts across this and failover origins can be controlled with maxAttemptsTimeout.

        The last valid, non-retried response from all origins will be returned to the client.
        If no origin returns a valid response, an HTTP 502 will be returned to the client.

        Defaults to 1. Must be a value greater than 0 and less than 4.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#max_attempts GoogleNetworkServicesEdgeCacheOrigin#max_attempts}
        '''
        result = self._values.get("max_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def origin_override_action(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction"]:
        '''origin_override_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#origin_override_action GoogleNetworkServicesEdgeCacheOrigin#origin_override_action}
        '''
        result = self._values.get("origin_override_action")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction"], result)

    @builtins.property
    def origin_redirect(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheOriginOriginRedirect"]:
        '''origin_redirect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#origin_redirect GoogleNetworkServicesEdgeCacheOrigin#origin_redirect}
        '''
        result = self._values.get("origin_redirect")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheOriginOriginRedirect"], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port to connect to the origin on.

        Defaults to port 443 for HTTP2 and HTTPS protocols, and port 80 for HTTP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#port GoogleNetworkServicesEdgeCacheOrigin#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#project GoogleNetworkServicesEdgeCacheOrigin#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol to use to connect to the configured origin.

        Defaults to HTTP2, and it is strongly recommended that users use HTTP2 for both security & performance.

        When using HTTP2 or HTTPS as the protocol, a valid, publicly-signed, unexpired TLS (SSL) certificate must be presented by the origin server. Possible values: ["HTTP2", "HTTPS", "HTTP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#protocol GoogleNetworkServicesEdgeCacheOrigin#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_conditions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies one or more retry conditions for the configured origin.

        If the failure mode during a connection attempt to the origin matches the configured retryCondition(s),
        the origin request will be retried up to maxAttempts times. The failoverOrigin, if configured, will then be used to satisfy the request.

        The default retryCondition is "CONNECT_FAILURE".

        retryConditions apply to this origin, and not subsequent failoverOrigin(s),
        which may specify their own retryConditions and maxAttempts.

        Valid values are:

        - CONNECT_FAILURE: Retry on failures connecting to origins, for example due to connection timeouts.
        - HTTP_5XX: Retry if the origin responds with any 5xx response code, or if the origin does not respond at all, example: disconnects, reset, read timeout, connection failure, and refused streams.
        - GATEWAY_ERROR: Similar to 5xx, but only applies to response codes 502, 503 or 504.
        - RETRIABLE_4XX: Retry for retriable 4xx response codes, which include HTTP 409 (Conflict) and HTTP 429 (Too Many Requests)
        - NOT_FOUND: Retry if the origin returns a HTTP 404 (Not Found). This can be useful when generating video content, and the segment is not available yet.
        - FORBIDDEN: Retry if the origin returns a HTTP 403 (Forbidden). Possible values: ["CONNECT_FAILURE", "HTTP_5XX", "GATEWAY_ERROR", "RETRIABLE_4XX", "NOT_FOUND", "FORBIDDEN"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#retry_conditions GoogleNetworkServicesEdgeCacheOrigin#retry_conditions}
        '''
        result = self._values.get("retry_conditions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional["GoogleNetworkServicesEdgeCacheOriginTimeout"]:
        '''timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#timeout GoogleNetworkServicesEdgeCacheOrigin#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheOriginTimeout"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheOriginTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#timeouts GoogleNetworkServicesEdgeCacheOrigin#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheOriginTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheOriginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginFlexShielding",
    jsii_struct_bases=[],
    name_mapping={"flex_shielding_regions": "flexShieldingRegions"},
)
class GoogleNetworkServicesEdgeCacheOriginFlexShielding:
    def __init__(
        self,
        *,
        flex_shielding_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param flex_shielding_regions: Whenever possible, content will be fetched from origin and cached in or near the specified origin. Best effort. You must specify exactly one FlexShieldingRegion. Possible values: ["AFRICA_SOUTH1", "ME_CENTRAL1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#flex_shielding_regions GoogleNetworkServicesEdgeCacheOrigin#flex_shielding_regions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f743d2761a006a3f06ec629eb4581ed484dae4d04dcea34544885912d90547e1)
            check_type(argname="argument flex_shielding_regions", value=flex_shielding_regions, expected_type=type_hints["flex_shielding_regions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if flex_shielding_regions is not None:
            self._values["flex_shielding_regions"] = flex_shielding_regions

    @builtins.property
    def flex_shielding_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Whenever possible, content will be fetched from origin and cached in or near the specified origin. Best effort.

        You must specify exactly one FlexShieldingRegion. Possible values: ["AFRICA_SOUTH1", "ME_CENTRAL1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#flex_shielding_regions GoogleNetworkServicesEdgeCacheOrigin#flex_shielding_regions}
        '''
        result = self._values.get("flex_shielding_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheOriginFlexShielding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheOriginFlexShieldingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginFlexShieldingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df8296c995d9a5d87d64daca1253f8fcd435ec86601d9f4d74e0c7fb22534060)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFlexShieldingRegions")
    def reset_flex_shielding_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlexShieldingRegions", []))

    @builtins.property
    @jsii.member(jsii_name="flexShieldingRegionsInput")
    def flex_shielding_regions_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "flexShieldingRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="flexShieldingRegions")
    def flex_shielding_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "flexShieldingRegions"))

    @flex_shielding_regions.setter
    def flex_shielding_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d240b0e0a2045f440aa5c148d013c97b6aa8e2da9a0a6c8179a24b08ef972a37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flexShieldingRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheOriginFlexShielding]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheOriginFlexShielding], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheOriginFlexShielding],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e94e45982d5f14b351bead80d01a2fa7be560e1a92946d74f23b035b8a56ed95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction",
    jsii_struct_bases=[],
    name_mapping={"header_action": "headerAction", "url_rewrite": "urlRewrite"},
)
class GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction:
    def __init__(
        self,
        *,
        header_action: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction", typing.Dict[builtins.str, typing.Any]]] = None,
        url_rewrite: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param header_action: header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#header_action GoogleNetworkServicesEdgeCacheOrigin#header_action}
        :param url_rewrite: url_rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#url_rewrite GoogleNetworkServicesEdgeCacheOrigin#url_rewrite}
        '''
        if isinstance(header_action, dict):
            header_action = GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction(**header_action)
        if isinstance(url_rewrite, dict):
            url_rewrite = GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite(**url_rewrite)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc9425f600c51b99c8540de9352b1bb2dbb70ccc03b11ce4a9c566d1591df877)
            check_type(argname="argument header_action", value=header_action, expected_type=type_hints["header_action"])
            check_type(argname="argument url_rewrite", value=url_rewrite, expected_type=type_hints["url_rewrite"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_action is not None:
            self._values["header_action"] = header_action
        if url_rewrite is not None:
            self._values["url_rewrite"] = url_rewrite

    @builtins.property
    def header_action(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction"]:
        '''header_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#header_action GoogleNetworkServicesEdgeCacheOrigin#header_action}
        '''
        result = self._values.get("header_action")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction"], result)

    @builtins.property
    def url_rewrite(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite"]:
        '''url_rewrite block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#url_rewrite GoogleNetworkServicesEdgeCacheOrigin#url_rewrite}
        '''
        result = self._values.get("url_rewrite")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction",
    jsii_struct_bases=[],
    name_mapping={"request_headers_to_add": "requestHeadersToAdd"},
)
class GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction:
    def __init__(
        self,
        *,
        request_headers_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param request_headers_to_add: request_headers_to_add block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#request_headers_to_add GoogleNetworkServicesEdgeCacheOrigin#request_headers_to_add}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c403624e11f9c0e3350818a70aa20d1cd67a4c1561da9b2baf49d3e582610a)
            check_type(argname="argument request_headers_to_add", value=request_headers_to_add, expected_type=type_hints["request_headers_to_add"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if request_headers_to_add is not None:
            self._values["request_headers_to_add"] = request_headers_to_add

    @builtins.property
    def request_headers_to_add(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd"]]]:
        '''request_headers_to_add block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#request_headers_to_add GoogleNetworkServicesEdgeCacheOrigin#request_headers_to_add}
        '''
        result = self._values.get("request_headers_to_add")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef100dbaf36bf104d6f8bcbf8c64a5375a91dc9b58e5eeaae16d0c84b868124a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequestHeadersToAdd")
    def put_request_headers_to_add(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b648a9408518a2cc38399ea494dd92ff5fe989ccf7f4414b4bbcc5f3e1e2a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeadersToAdd", [value]))

    @jsii.member(jsii_name="resetRequestHeadersToAdd")
    def reset_request_headers_to_add(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeadersToAdd", []))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersToAdd")
    def request_headers_to_add(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddList":
        return typing.cast("GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddList", jsii.get(self, "requestHeadersToAdd"))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersToAddInput")
    def request_headers_to_add_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd"]]], jsii.get(self, "requestHeadersToAddInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b89f9153c37b3d92c9d510cbee9e87868e354248e8f537588ac3ae31568fc1f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd",
    jsii_struct_bases=[],
    name_mapping={
        "header_name": "headerName",
        "header_value": "headerValue",
        "replace": "replace",
    },
)
class GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        header_value: builtins.str,
        replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param header_name: The name of the header to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#header_name GoogleNetworkServicesEdgeCacheOrigin#header_name}
        :param header_value: The value of the header to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#header_value GoogleNetworkServicesEdgeCacheOrigin#header_value}
        :param replace: Whether to replace all existing headers with the same name. By default, added header values are appended to the response or request headers with the same field names. The added values are separated by commas. To overwrite existing values, set 'replace' to 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#replace GoogleNetworkServicesEdgeCacheOrigin#replace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0db419fa1a555506168fe599bc862ab89246b58ccdc1e0346122aeafa23965)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#header_name GoogleNetworkServicesEdgeCacheOrigin#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header_value(self) -> builtins.str:
        '''The value of the header to add.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#header_value GoogleNetworkServicesEdgeCacheOrigin#header_value}
        '''
        result = self._values.get("header_value")
        assert result is not None, "Required property 'header_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replace(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to replace all existing headers with the same name.

        By default, added header values are appended
        to the response or request headers with the
        same field names. The added values are
        separated by commas.

        To overwrite existing values, set 'replace' to 'true'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#replace GoogleNetworkServicesEdgeCacheOrigin#replace}
        '''
        result = self._values.get("replace")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23f3a506302c3499a5c23958380999d196bfbd2000017dc0dd959c3aed4843c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__242aab38697ad7f9e09e0b91b8140944c302ed46f9693c79c2ff8b5e4809b3c1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ac2346e963fc71e183f872579381169c9ac02b2f79d3a1ce2268f4183a28d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc1f76ce1ddddecde648d8d6c08fd63e6e70f9c25349b460018080164cae6034)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9890ec191dca800e85ac26765784ca93497b07d7c808ec4df8f053076a35773f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f72963a48c5408aed4436383a10e6cf7b7b42945f431b4638dbf56f4b18e8d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8342d8fc97c5d97da8c299784e066b02e6ce57a167bbe142e544cc0a84b5670)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ebde985f83ab60bc6cbd777b151914db3bcb84fae9a41dc1a84f918d6ddbc1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))

    @header_value.setter
    def header_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d279f85372ab55da94aa7e32cd2f001201a3365dbb8aaaa0d445c1c7d74afe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6c992f1785db71dfee519483f93878809b01788823174284e892aebb6288da7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c74d02df26b189dc1128c360813264748d1991d3e01b6fe815915e8a6b3d871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19a28e995af969c37db70800075a49e3b491f01f41b8cbf29cb399060069e79c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaderAction")
    def put_header_action(
        self,
        *,
        request_headers_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param request_headers_to_add: request_headers_to_add block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#request_headers_to_add GoogleNetworkServicesEdgeCacheOrigin#request_headers_to_add}
        '''
        value = GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction(
            request_headers_to_add=request_headers_to_add
        )

        return typing.cast(None, jsii.invoke(self, "putHeaderAction", [value]))

    @jsii.member(jsii_name="putUrlRewrite")
    def put_url_rewrite(
        self,
        *,
        host_rewrite: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_rewrite: Prior to forwarding the request to the selected origin, the request's host header is replaced with contents of the hostRewrite. This value must be between 1 and 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#host_rewrite GoogleNetworkServicesEdgeCacheOrigin#host_rewrite}
        '''
        value = GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite(
            host_rewrite=host_rewrite
        )

        return typing.cast(None, jsii.invoke(self, "putUrlRewrite", [value]))

    @jsii.member(jsii_name="resetHeaderAction")
    def reset_header_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderAction", []))

    @jsii.member(jsii_name="resetUrlRewrite")
    def reset_url_rewrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlRewrite", []))

    @builtins.property
    @jsii.member(jsii_name="headerAction")
    def header_action(
        self,
    ) -> GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionOutputReference:
        return typing.cast(GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionOutputReference, jsii.get(self, "headerAction"))

    @builtins.property
    @jsii.member(jsii_name="urlRewrite")
    def url_rewrite(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewriteOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewriteOutputReference", jsii.get(self, "urlRewrite"))

    @builtins.property
    @jsii.member(jsii_name="headerActionInput")
    def header_action_input(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction], jsii.get(self, "headerActionInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRewriteInput")
    def url_rewrite_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite"], jsii.get(self, "urlRewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfdea8fe99fee33a27b27e4151bd4a4e60623baffef019ccb2c580c7ebc0fa76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite",
    jsii_struct_bases=[],
    name_mapping={"host_rewrite": "hostRewrite"},
)
class GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite:
    def __init__(self, *, host_rewrite: typing.Optional[builtins.str] = None) -> None:
        '''
        :param host_rewrite: Prior to forwarding the request to the selected origin, the request's host header is replaced with contents of the hostRewrite. This value must be between 1 and 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#host_rewrite GoogleNetworkServicesEdgeCacheOrigin#host_rewrite}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c53bdf3abf502457dd47c22346a62ae2030463e94dae1928c728bd8a10ce3432)
            check_type(argname="argument host_rewrite", value=host_rewrite, expected_type=type_hints["host_rewrite"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host_rewrite is not None:
            self._values["host_rewrite"] = host_rewrite

    @builtins.property
    def host_rewrite(self) -> typing.Optional[builtins.str]:
        '''Prior to forwarding the request to the selected origin, the request's host header is replaced with contents of the hostRewrite.

        This value must be between 1 and 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#host_rewrite GoogleNetworkServicesEdgeCacheOrigin#host_rewrite}
        '''
        result = self._values.get("host_rewrite")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewriteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewriteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d84e96928c13bd2960008799696af03a228f2e3fba2f825095ff95b9348db78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHostRewrite")
    def reset_host_rewrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostRewrite", []))

    @builtins.property
    @jsii.member(jsii_name="hostRewriteInput")
    def host_rewrite_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostRewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="hostRewrite")
    def host_rewrite(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostRewrite"))

    @host_rewrite.setter
    def host_rewrite(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae534a010fcf04a520bba13631137f660b7da13a7bcbd3ee614585909fbe22c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostRewrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9819762cd360218839dab22ea3ecf181e9aa1c340093f3987bf74e42f1e3b093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginOriginRedirect",
    jsii_struct_bases=[],
    name_mapping={"redirect_conditions": "redirectConditions"},
)
class GoogleNetworkServicesEdgeCacheOriginOriginRedirect:
    def __init__(
        self,
        *,
        redirect_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param redirect_conditions: The set of redirect response codes that the CDN follows. Values of `RedirectConditions <https://cloud.google.com/media-cdn/docs/reference/rest/v1/projects.locations.edgeCacheOrigins#redirectconditions>`_ are accepted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#redirect_conditions GoogleNetworkServicesEdgeCacheOrigin#redirect_conditions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f7c3669111fcb71c28b88d12a59e2ca788365c391a037a871a2dc69e74fa43)
            check_type(argname="argument redirect_conditions", value=redirect_conditions, expected_type=type_hints["redirect_conditions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if redirect_conditions is not None:
            self._values["redirect_conditions"] = redirect_conditions

    @builtins.property
    def redirect_conditions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of redirect response codes that the CDN follows. Values of `RedirectConditions <https://cloud.google.com/media-cdn/docs/reference/rest/v1/projects.locations.edgeCacheOrigins#redirectconditions>`_ are accepted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#redirect_conditions GoogleNetworkServicesEdgeCacheOrigin#redirect_conditions}
        '''
        result = self._values.get("redirect_conditions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheOriginOriginRedirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheOriginOriginRedirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginOriginRedirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5bf88ff8d3fd4789ed824be36cf66b22f090f18cf1d27c8efcd14de05f61eb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRedirectConditions")
    def reset_redirect_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectConditions", []))

    @builtins.property
    @jsii.member(jsii_name="redirectConditionsInput")
    def redirect_conditions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "redirectConditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectConditions")
    def redirect_conditions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "redirectConditions"))

    @redirect_conditions.setter
    def redirect_conditions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9ce2fc730ca3851916ed7436ed77cac865d03562b3d08482cdcb39bfa6f226c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectConditions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginRedirect]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginRedirect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginRedirect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa699286b9118f6a4a0bdfc4a65b38e9fa8e0e24b41236cdbf803dc66e09f70c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginTimeout",
    jsii_struct_bases=[],
    name_mapping={
        "connect_timeout": "connectTimeout",
        "max_attempts_timeout": "maxAttemptsTimeout",
        "read_timeout": "readTimeout",
        "response_timeout": "responseTimeout",
    },
)
class GoogleNetworkServicesEdgeCacheOriginTimeout:
    def __init__(
        self,
        *,
        connect_timeout: typing.Optional[builtins.str] = None,
        max_attempts_timeout: typing.Optional[builtins.str] = None,
        read_timeout: typing.Optional[builtins.str] = None,
        response_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connect_timeout: The maximum duration to wait for a single origin connection to be established, including DNS lookup, TLS handshake and TCP/QUIC connection establishment. Defaults to 5 seconds. The timeout must be a value between 1s and 15s. The connectTimeout capped by the deadline set by the request's maxAttemptsTimeout. The last connection attempt may have a smaller connectTimeout in order to adhere to the overall maxAttemptsTimeout. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#connect_timeout GoogleNetworkServicesEdgeCacheOrigin#connect_timeout}
        :param max_attempts_timeout: The maximum time across all connection attempts to the origin, including failover origins, before returning an error to the client. A HTTP 504 will be returned if the timeout is reached before a response is returned. Defaults to 15 seconds. The timeout must be a value between 1s and 30s. If a failoverOrigin is specified, the maxAttemptsTimeout of the first configured origin sets the deadline for all connection attempts across all failoverOrigins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#max_attempts_timeout GoogleNetworkServicesEdgeCacheOrigin#max_attempts_timeout}
        :param read_timeout: The maximum duration to wait between reads of a single HTTP connection/stream. Defaults to 15 seconds. The timeout must be a value between 1s and 30s. The readTimeout is capped by the responseTimeout. All reads of the HTTP connection/stream must be completed by the deadline set by the responseTimeout. If the response headers have already been written to the connection, the response will be truncated and logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#read_timeout GoogleNetworkServicesEdgeCacheOrigin#read_timeout}
        :param response_timeout: The maximum duration to wait for the last byte of a response to arrive when reading from the HTTP connection/stream. Defaults to 30 seconds. The timeout must be a value between 1s and 120s. The responseTimeout starts after the connection has been established. This also applies to HTTP Chunked Transfer Encoding responses, and/or when an open-ended Range request is made to the origin. Origins that take longer to write additional bytes to the response than the configured responseTimeout will result in an error being returned to the client. If the response headers have already been written to the connection, the response will be truncated and logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#response_timeout GoogleNetworkServicesEdgeCacheOrigin#response_timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c6debcfebe5843a22d6f63d1dbbce8d1042305d6b2debbc893444dc4aa0e083)
            check_type(argname="argument connect_timeout", value=connect_timeout, expected_type=type_hints["connect_timeout"])
            check_type(argname="argument max_attempts_timeout", value=max_attempts_timeout, expected_type=type_hints["max_attempts_timeout"])
            check_type(argname="argument read_timeout", value=read_timeout, expected_type=type_hints["read_timeout"])
            check_type(argname="argument response_timeout", value=response_timeout, expected_type=type_hints["response_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connect_timeout is not None:
            self._values["connect_timeout"] = connect_timeout
        if max_attempts_timeout is not None:
            self._values["max_attempts_timeout"] = max_attempts_timeout
        if read_timeout is not None:
            self._values["read_timeout"] = read_timeout
        if response_timeout is not None:
            self._values["response_timeout"] = response_timeout

    @builtins.property
    def connect_timeout(self) -> typing.Optional[builtins.str]:
        '''The maximum duration to wait for a single origin connection to be established, including DNS lookup, TLS handshake and TCP/QUIC connection establishment.

        Defaults to 5 seconds. The timeout must be a value between 1s and 15s.

        The connectTimeout capped by the deadline set by the request's maxAttemptsTimeout.  The last connection attempt may have a smaller connectTimeout in order to adhere to the overall maxAttemptsTimeout.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#connect_timeout GoogleNetworkServicesEdgeCacheOrigin#connect_timeout}
        '''
        result = self._values.get("connect_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_attempts_timeout(self) -> typing.Optional[builtins.str]:
        '''The maximum time across all connection attempts to the origin, including failover origins, before returning an error to the client.

        A HTTP 504 will be returned if the timeout is reached before a response is returned.

        Defaults to 15 seconds. The timeout must be a value between 1s and 30s.

        If a failoverOrigin is specified, the maxAttemptsTimeout of the first configured origin sets the deadline for all connection attempts across all failoverOrigins.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#max_attempts_timeout GoogleNetworkServicesEdgeCacheOrigin#max_attempts_timeout}
        '''
        result = self._values.get("max_attempts_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_timeout(self) -> typing.Optional[builtins.str]:
        '''The maximum duration to wait between reads of a single HTTP connection/stream.

        Defaults to 15 seconds.  The timeout must be a value between 1s and 30s.

        The readTimeout is capped by the responseTimeout.  All reads of the HTTP connection/stream must be completed by the deadline set by the responseTimeout.

        If the response headers have already been written to the connection, the response will be truncated and logged.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#read_timeout GoogleNetworkServicesEdgeCacheOrigin#read_timeout}
        '''
        result = self._values.get("read_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_timeout(self) -> typing.Optional[builtins.str]:
        '''The maximum duration to wait for the last byte of a response to arrive when reading from the HTTP connection/stream.

        Defaults to 30 seconds. The timeout must be a value between 1s and 120s.

        The responseTimeout starts after the connection has been established.

        This also applies to HTTP Chunked Transfer Encoding responses, and/or when an open-ended Range request is made to the origin. Origins that take longer to write additional bytes to the response than the configured responseTimeout will result in an error being returned to the client.

        If the response headers have already been written to the connection, the response will be truncated and logged.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#response_timeout GoogleNetworkServicesEdgeCacheOrigin#response_timeout}
        '''
        result = self._values.get("response_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheOriginTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheOriginTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__029b68a81578562da3dc232ad91623c6f091304654be063dde3689951749db0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConnectTimeout")
    def reset_connect_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectTimeout", []))

    @jsii.member(jsii_name="resetMaxAttemptsTimeout")
    def reset_max_attempts_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAttemptsTimeout", []))

    @jsii.member(jsii_name="resetReadTimeout")
    def reset_read_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadTimeout", []))

    @jsii.member(jsii_name="resetResponseTimeout")
    def reset_response_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="connectTimeoutInput")
    def connect_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAttemptsTimeoutInput")
    def max_attempts_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxAttemptsTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="readTimeoutInput")
    def read_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="responseTimeoutInput")
    def response_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="connectTimeout")
    def connect_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectTimeout"))

    @connect_timeout.setter
    def connect_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f0b87cfc7afe31e0afc30d7f314fdedc0b5a6fa459d6008425c5d7100050f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAttemptsTimeout")
    def max_attempts_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxAttemptsTimeout"))

    @max_attempts_timeout.setter
    def max_attempts_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caeba8bd7d86641f1c1cd7ca5356dea66da8f16a1c2a12213488a91a4111785f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAttemptsTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readTimeout")
    def read_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readTimeout"))

    @read_timeout.setter
    def read_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eceef2870d41979a73f154e6b6aa669f03b4a7e3254c9f89361cfefb3a2131c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseTimeout")
    def response_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseTimeout"))

    @response_timeout.setter
    def response_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6a00608ccc7eadfc2cdcfdd32a5505eb019a67934a9e71a5f5533444c1de99b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheOriginTimeout]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheOriginTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheOriginTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f10a79a3992d969925839e43b65cf04b014389ab537455244abc2b731c866d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNetworkServicesEdgeCacheOriginTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#create GoogleNetworkServicesEdgeCacheOrigin#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#delete GoogleNetworkServicesEdgeCacheOrigin#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#update GoogleNetworkServicesEdgeCacheOrigin#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3279a86ef0264d66c2f3a6537e244e6b4576d0860cb7c72001d47edcaafc468a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#create GoogleNetworkServicesEdgeCacheOrigin#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#delete GoogleNetworkServicesEdgeCacheOrigin#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_origin#update GoogleNetworkServicesEdgeCacheOrigin#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheOriginTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheOriginTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheOrigin.GoogleNetworkServicesEdgeCacheOriginTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a382c6ec59138ed08df05fe9ae084a4618f460a245ed9e431b270045d9f27938)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0634fc0cf9d47c499427006ee59a0eec6270d97160d173e6e0154d57157afc35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1557eee738bf65b2a99476028f657572cd627d5e6c13a3cf1c7a7b5c41a67f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18da26050f2c42aa9e7cf6332f773d6ffd5b15951dbd42671705f96724c75b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheOriginTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheOriginTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheOriginTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c989ea339f157d178dd5ed6b5275f578b08ccc0c78a069c98dd25632c3446f4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleNetworkServicesEdgeCacheOrigin",
    "GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication",
    "GoogleNetworkServicesEdgeCacheOriginAwsV4AuthenticationOutputReference",
    "GoogleNetworkServicesEdgeCacheOriginConfig",
    "GoogleNetworkServicesEdgeCacheOriginFlexShielding",
    "GoogleNetworkServicesEdgeCacheOriginFlexShieldingOutputReference",
    "GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction",
    "GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction",
    "GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionOutputReference",
    "GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd",
    "GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddList",
    "GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddOutputReference",
    "GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionOutputReference",
    "GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite",
    "GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewriteOutputReference",
    "GoogleNetworkServicesEdgeCacheOriginOriginRedirect",
    "GoogleNetworkServicesEdgeCacheOriginOriginRedirectOutputReference",
    "GoogleNetworkServicesEdgeCacheOriginTimeout",
    "GoogleNetworkServicesEdgeCacheOriginTimeoutOutputReference",
    "GoogleNetworkServicesEdgeCacheOriginTimeouts",
    "GoogleNetworkServicesEdgeCacheOriginTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6edf6d811003f0d49b47da92d641f38476538f976897594107c7af11fd124bc5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    origin_address: builtins.str,
    aws_v4_authentication: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    failover_origin: typing.Optional[builtins.str] = None,
    flex_shielding: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheOriginFlexShielding, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_attempts: typing.Optional[jsii.Number] = None,
    origin_override_action: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction, typing.Dict[builtins.str, typing.Any]]] = None,
    origin_redirect: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheOriginOriginRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeout: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheOriginTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheOriginTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__12548fec5e913d72d6205ebdc945d2bf28f9211cf65ce0aff707f15276880740(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39bdee2717886a78ea10ed0bfe88a615b1d255ca1a92e9e574c89906bef1f07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d09a38137560a2e9788df7aa56fc28afc056bc6837de6f889b233ae29bc78a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c474d60b4882a22782e41845e494f55ed8389165e805a251aec82b18fae792(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e5b76fe9f9639351030e98e70e93c23eb8cc68067fe387933252fb722ec83c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4841fab67b7bc8a526001d38dabf2d40496af58540f39ab8d7978162d33a25(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f952c7027c8b10d79fc19ecbf5acdd8c62062637d87e985a0a793807133b77b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42cf73349191780bbdfa2fc083155fbe1cd37e2a672ebd50408212ccf7cedb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da9109b4ee2e1d0b1adc67da5fb0e068e79cefbcd560605b56f486e04464b1b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09230361e43a53221a7af8ea498cec2bb910a6e397dd13efaa0215ca56caf91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddfae4d7d6b6263408f7d28d92094ee538d7894b0c10310eed1c84d1d604ab6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92eeb0d206432d00377ce1eac8c73f7c90245266d6d71e6f576190a5dce00c7a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37da7508515c5002e8db578e2074d88f098a82e2f885f6627f1e4cd2f31fa42(
    *,
    access_key_id: builtins.str,
    origin_region: builtins.str,
    secret_access_key_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90dec2c7153ea3e3a1ecb457aef42f642d1907a637ba926d98841e8c085b509d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34828e6d5247679ec270cfe738666945f1e1b19e1a70c98d6191b7d4f50bbf32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86fc984fdaf02eb9bc05f218cc080d33e1c946b9f12aade064edbd1e9433d5bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f2f0ec64ce57827efb93376bb690801b2830e117108023c0e959cc88f54710(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fef23eb20fc90b564a990302ecb2e7978dbf760f85c405b8e195a9e05233b9f(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2897b17b9a743f41d006328108815afbb72c2572dccbce491858f0b655dcff94(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    origin_address: builtins.str,
    aws_v4_authentication: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheOriginAwsV4Authentication, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    failover_origin: typing.Optional[builtins.str] = None,
    flex_shielding: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheOriginFlexShielding, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_attempts: typing.Optional[jsii.Number] = None,
    origin_override_action: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction, typing.Dict[builtins.str, typing.Any]]] = None,
    origin_redirect: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheOriginOriginRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeout: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheOriginTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheOriginTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f743d2761a006a3f06ec629eb4581ed484dae4d04dcea34544885912d90547e1(
    *,
    flex_shielding_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8296c995d9a5d87d64daca1253f8fcd435ec86601d9f4d74e0c7fb22534060(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d240b0e0a2045f440aa5c148d013c97b6aa8e2da9a0a6c8179a24b08ef972a37(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e94e45982d5f14b351bead80d01a2fa7be560e1a92946d74f23b035b8a56ed95(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheOriginFlexShielding],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc9425f600c51b99c8540de9352b1bb2dbb70ccc03b11ce4a9c566d1591df877(
    *,
    header_action: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction, typing.Dict[builtins.str, typing.Any]]] = None,
    url_rewrite: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c403624e11f9c0e3350818a70aa20d1cd67a4c1561da9b2baf49d3e582610a(
    *,
    request_headers_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef100dbaf36bf104d6f8bcbf8c64a5375a91dc9b58e5eeaae16d0c84b868124a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b648a9408518a2cc38399ea494dd92ff5fe989ccf7f4414b4bbcc5f3e1e2a2b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89f9153c37b3d92c9d510cbee9e87868e354248e8f537588ac3ae31568fc1f8(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0db419fa1a555506168fe599bc862ab89246b58ccdc1e0346122aeafa23965(
    *,
    header_name: builtins.str,
    header_value: builtins.str,
    replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f3a506302c3499a5c23958380999d196bfbd2000017dc0dd959c3aed4843c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242aab38697ad7f9e09e0b91b8140944c302ed46f9693c79c2ff8b5e4809b3c1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ac2346e963fc71e183f872579381169c9ac02b2f79d3a1ce2268f4183a28d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1f76ce1ddddecde648d8d6c08fd63e6e70f9c25349b460018080164cae6034(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9890ec191dca800e85ac26765784ca93497b07d7c808ec4df8f053076a35773f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72963a48c5408aed4436383a10e6cf7b7b42945f431b4638dbf56f4b18e8d88(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8342d8fc97c5d97da8c299784e066b02e6ce57a167bbe142e544cc0a84b5670(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ebde985f83ab60bc6cbd777b151914db3bcb84fae9a41dc1a84f918d6ddbc1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d279f85372ab55da94aa7e32cd2f001201a3365dbb8aaaa0d445c1c7d74afe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c992f1785db71dfee519483f93878809b01788823174284e892aebb6288da7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c74d02df26b189dc1128c360813264748d1991d3e01b6fe815915e8a6b3d871(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a28e995af969c37db70800075a49e3b491f01f41b8cbf29cb399060069e79c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfdea8fe99fee33a27b27e4151bd4a4e60623baffef019ccb2c580c7ebc0fa76(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginOverrideAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53bdf3abf502457dd47c22346a62ae2030463e94dae1928c728bd8a10ce3432(
    *,
    host_rewrite: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d84e96928c13bd2960008799696af03a228f2e3fba2f825095ff95b9348db78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae534a010fcf04a520bba13631137f660b7da13a7bcbd3ee614585909fbe22c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9819762cd360218839dab22ea3ecf181e9aa1c340093f3987bf74e42f1e3b093(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f7c3669111fcb71c28b88d12a59e2ca788365c391a037a871a2dc69e74fa43(
    *,
    redirect_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5bf88ff8d3fd4789ed824be36cf66b22f090f18cf1d27c8efcd14de05f61eb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ce2fc730ca3851916ed7436ed77cac865d03562b3d08482cdcb39bfa6f226c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa699286b9118f6a4a0bdfc4a65b38e9fa8e0e24b41236cdbf803dc66e09f70c(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheOriginOriginRedirect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c6debcfebe5843a22d6f63d1dbbce8d1042305d6b2debbc893444dc4aa0e083(
    *,
    connect_timeout: typing.Optional[builtins.str] = None,
    max_attempts_timeout: typing.Optional[builtins.str] = None,
    read_timeout: typing.Optional[builtins.str] = None,
    response_timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029b68a81578562da3dc232ad91623c6f091304654be063dde3689951749db0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f0b87cfc7afe31e0afc30d7f314fdedc0b5a6fa459d6008425c5d7100050f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caeba8bd7d86641f1c1cd7ca5356dea66da8f16a1c2a12213488a91a4111785f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eceef2870d41979a73f154e6b6aa669f03b4a7e3254c9f89361cfefb3a2131c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a00608ccc7eadfc2cdcfdd32a5505eb019a67934a9e71a5f5533444c1de99b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f10a79a3992d969925839e43b65cf04b014389ab537455244abc2b731c866d(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheOriginTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3279a86ef0264d66c2f3a6537e244e6b4576d0860cb7c72001d47edcaafc468a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a382c6ec59138ed08df05fe9ae084a4618f460a245ed9e431b270045d9f27938(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0634fc0cf9d47c499427006ee59a0eec6270d97160d173e6e0154d57157afc35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1557eee738bf65b2a99476028f657572cd627d5e6c13a3cf1c7a7b5c41a67f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18da26050f2c42aa9e7cf6332f773d6ffd5b15951dbd42671705f96724c75b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c989ea339f157d178dd5ed6b5275f578b08ccc0c78a069c98dd25632c3446f4d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheOriginTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
