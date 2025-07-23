r'''
# `google_network_services_edge_cache_origin`

Refer to the Terraform Registry for docs: [`google_network_services_edge_cache_origin`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin).
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


class NetworkServicesEdgeCacheOrigin(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOrigin",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin google_network_services_edge_cache_origin}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        origin_address: builtins.str,
        aws_v4_authentication: typing.Optional[typing.Union["NetworkServicesEdgeCacheOriginAwsV4Authentication", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        failover_origin: typing.Optional[builtins.str] = None,
        flex_shielding: typing.Optional[typing.Union["NetworkServicesEdgeCacheOriginFlexShielding", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_attempts: typing.Optional[jsii.Number] = None,
        origin_override_action: typing.Optional[typing.Union["NetworkServicesEdgeCacheOriginOriginOverrideAction", typing.Dict[builtins.str, typing.Any]]] = None,
        origin_redirect: typing.Optional[typing.Union["NetworkServicesEdgeCacheOriginOriginRedirect", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout: typing.Optional[typing.Union["NetworkServicesEdgeCacheOriginTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["NetworkServicesEdgeCacheOriginTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin google_network_services_edge_cache_origin} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#name NetworkServicesEdgeCacheOrigin#name}
        :param origin_address: A fully qualified domain name (FQDN) or IP address reachable over the public Internet, or the address of a Google Cloud Storage bucket. This address will be used as the origin for cache requests - e.g. FQDN: media-backend.example.com, IPv4: 35.218.1.1, IPv6: 2607:f8b0:4012:809::200e, Cloud Storage: gs://bucketname When providing an FQDN (hostname), it must be publicly resolvable (e.g. via Google public DNS) and IP addresses must be publicly routable. It must not contain a protocol (e.g., https://) and it must not contain any slashes. If a Cloud Storage bucket is provided, it must be in the canonical "gs://bucketname" format. Other forms, such as "storage.googleapis.com", will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#origin_address NetworkServicesEdgeCacheOrigin#origin_address}
        :param aws_v4_authentication: aws_v4_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#aws_v4_authentication NetworkServicesEdgeCacheOrigin#aws_v4_authentication}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#description NetworkServicesEdgeCacheOrigin#description}
        :param failover_origin: The Origin resource to try when the current origin cannot be reached. After maxAttempts is reached, the configured failoverOrigin will be used to fulfil the request. The value of timeout.maxAttemptsTimeout dictates the timeout across all origins. A reference to a Topic resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#failover_origin NetworkServicesEdgeCacheOrigin#failover_origin}
        :param flex_shielding: flex_shielding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#flex_shielding NetworkServicesEdgeCacheOrigin#flex_shielding}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#id NetworkServicesEdgeCacheOrigin#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the EdgeCache resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#labels NetworkServicesEdgeCacheOrigin#labels}
        :param max_attempts: The maximum number of attempts to cache fill from this origin. Another attempt is made when a cache fill fails with one of the retryConditions. Once maxAttempts to this origin have failed the failoverOrigin will be used, if one is specified. That failoverOrigin may specify its own maxAttempts, retryConditions and failoverOrigin to control its own cache fill failures. The total number of allowed attempts to cache fill across this and failover origins is limited to four. The total time allowed for cache fill attempts across this and failover origins can be controlled with maxAttemptsTimeout. The last valid, non-retried response from all origins will be returned to the client. If no origin returns a valid response, an HTTP 502 will be returned to the client. Defaults to 1. Must be a value greater than 0 and less than 4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#max_attempts NetworkServicesEdgeCacheOrigin#max_attempts}
        :param origin_override_action: origin_override_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#origin_override_action NetworkServicesEdgeCacheOrigin#origin_override_action}
        :param origin_redirect: origin_redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#origin_redirect NetworkServicesEdgeCacheOrigin#origin_redirect}
        :param port: The port to connect to the origin on. Defaults to port 443 for HTTP2 and HTTPS protocols, and port 80 for HTTP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#port NetworkServicesEdgeCacheOrigin#port}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#project NetworkServicesEdgeCacheOrigin#project}.
        :param protocol: The protocol to use to connect to the configured origin. Defaults to HTTP2, and it is strongly recommended that users use HTTP2 for both security & performance. When using HTTP2 or HTTPS as the protocol, a valid, publicly-signed, unexpired TLS (SSL) certificate must be presented by the origin server. Possible values: ["HTTP2", "HTTPS", "HTTP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#protocol NetworkServicesEdgeCacheOrigin#protocol}
        :param retry_conditions: Specifies one or more retry conditions for the configured origin. If the failure mode during a connection attempt to the origin matches the configured retryCondition(s), the origin request will be retried up to maxAttempts times. The failoverOrigin, if configured, will then be used to satisfy the request. The default retryCondition is "CONNECT_FAILURE". retryConditions apply to this origin, and not subsequent failoverOrigin(s), which may specify their own retryConditions and maxAttempts. Valid values are: - CONNECT_FAILURE: Retry on failures connecting to origins, for example due to connection timeouts. - HTTP_5XX: Retry if the origin responds with any 5xx response code, or if the origin does not respond at all, example: disconnects, reset, read timeout, connection failure, and refused streams. - GATEWAY_ERROR: Similar to 5xx, but only applies to response codes 502, 503 or 504. - RETRIABLE_4XX: Retry for retriable 4xx response codes, which include HTTP 409 (Conflict) and HTTP 429 (Too Many Requests) - NOT_FOUND: Retry if the origin returns a HTTP 404 (Not Found). This can be useful when generating video content, and the segment is not available yet. - FORBIDDEN: Retry if the origin returns a HTTP 403 (Forbidden). Possible values: ["CONNECT_FAILURE", "HTTP_5XX", "GATEWAY_ERROR", "RETRIABLE_4XX", "NOT_FOUND", "FORBIDDEN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#retry_conditions NetworkServicesEdgeCacheOrigin#retry_conditions}
        :param timeout: timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#timeout NetworkServicesEdgeCacheOrigin#timeout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#timeouts NetworkServicesEdgeCacheOrigin#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c21df93d1996318f9c957070740c8d72e22c37e5bff3072eb29fb680a72cb2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkServicesEdgeCacheOriginConfig(
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
        '''Generates CDKTF code for importing a NetworkServicesEdgeCacheOrigin resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkServicesEdgeCacheOrigin to import.
        :param import_from_id: The id of the existing NetworkServicesEdgeCacheOrigin that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkServicesEdgeCacheOrigin to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0c9cb22d1d6da3c50e953c0b256bef0c7c9661ee5270c800c50c0c4d630f9f)
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
        :param access_key_id: The access key ID your origin uses to identify the key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#access_key_id NetworkServicesEdgeCacheOrigin#access_key_id}
        :param origin_region: The name of the AWS region that your origin is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#origin_region NetworkServicesEdgeCacheOrigin#origin_region}
        :param secret_access_key_version: The Secret Manager secret version of the secret access key used by your origin. This is the resource name of the secret version in the format 'projects/* /secrets/* /versions/*' where the '*' values are replaced by the project, secret, and version you require. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#secret_access_key_version NetworkServicesEdgeCacheOrigin#secret_access_key_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = NetworkServicesEdgeCacheOriginAwsV4Authentication(
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
        :param flex_shielding_regions: Whenever possible, content will be fetched from origin and cached in or near the specified origin. Best effort. You must specify exactly one FlexShieldingRegion. Possible values: ["AFRICA_SOUTH1", "ME_CENTRAL1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#flex_shielding_regions NetworkServicesEdgeCacheOrigin#flex_shielding_regions}
        '''
        value = NetworkServicesEdgeCacheOriginFlexShielding(
            flex_shielding_regions=flex_shielding_regions
        )

        return typing.cast(None, jsii.invoke(self, "putFlexShielding", [value]))

    @jsii.member(jsii_name="putOriginOverrideAction")
    def put_origin_override_action(
        self,
        *,
        header_action: typing.Optional[typing.Union["NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction", typing.Dict[builtins.str, typing.Any]]] = None,
        url_rewrite: typing.Optional[typing.Union["NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param header_action: header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#header_action NetworkServicesEdgeCacheOrigin#header_action}
        :param url_rewrite: url_rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#url_rewrite NetworkServicesEdgeCacheOrigin#url_rewrite}
        '''
        value = NetworkServicesEdgeCacheOriginOriginOverrideAction(
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
        :param redirect_conditions: The set of redirect response codes that the CDN follows. Values of `RedirectConditions <https://cloud.google.com/media-cdn/docs/reference/rest/v1/projects.locations.edgeCacheOrigins#redirectconditions>`_ are accepted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#redirect_conditions NetworkServicesEdgeCacheOrigin#redirect_conditions}
        '''
        value = NetworkServicesEdgeCacheOriginOriginRedirect(
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
        :param connect_timeout: The maximum duration to wait for a single origin connection to be established, including DNS lookup, TLS handshake and TCP/QUIC connection establishment. Defaults to 5 seconds. The timeout must be a value between 1s and 15s. The connectTimeout capped by the deadline set by the request's maxAttemptsTimeout. The last connection attempt may have a smaller connectTimeout in order to adhere to the overall maxAttemptsTimeout. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#connect_timeout NetworkServicesEdgeCacheOrigin#connect_timeout}
        :param max_attempts_timeout: The maximum time across all connection attempts to the origin, including failover origins, before returning an error to the client. A HTTP 504 will be returned if the timeout is reached before a response is returned. Defaults to 15 seconds. The timeout must be a value between 1s and 30s. If a failoverOrigin is specified, the maxAttemptsTimeout of the first configured origin sets the deadline for all connection attempts across all failoverOrigins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#max_attempts_timeout NetworkServicesEdgeCacheOrigin#max_attempts_timeout}
        :param read_timeout: The maximum duration to wait between reads of a single HTTP connection/stream. Defaults to 15 seconds. The timeout must be a value between 1s and 30s. The readTimeout is capped by the responseTimeout. All reads of the HTTP connection/stream must be completed by the deadline set by the responseTimeout. If the response headers have already been written to the connection, the response will be truncated and logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#read_timeout NetworkServicesEdgeCacheOrigin#read_timeout}
        :param response_timeout: The maximum duration to wait for the last byte of a response to arrive when reading from the HTTP connection/stream. Defaults to 30 seconds. The timeout must be a value between 1s and 120s. The responseTimeout starts after the connection has been established. This also applies to HTTP Chunked Transfer Encoding responses, and/or when an open-ended Range request is made to the origin. Origins that take longer to write additional bytes to the response than the configured responseTimeout will result in an error being returned to the client. If the response headers have already been written to the connection, the response will be truncated and logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#response_timeout NetworkServicesEdgeCacheOrigin#response_timeout}
        '''
        value = NetworkServicesEdgeCacheOriginTimeout(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#create NetworkServicesEdgeCacheOrigin#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#delete NetworkServicesEdgeCacheOrigin#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#update NetworkServicesEdgeCacheOrigin#update}.
        '''
        value = NetworkServicesEdgeCacheOriginTimeouts(
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
    ) -> "NetworkServicesEdgeCacheOriginAwsV4AuthenticationOutputReference":
        return typing.cast("NetworkServicesEdgeCacheOriginAwsV4AuthenticationOutputReference", jsii.get(self, "awsV4Authentication"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="flexShielding")
    def flex_shielding(
        self,
    ) -> "NetworkServicesEdgeCacheOriginFlexShieldingOutputReference":
        return typing.cast("NetworkServicesEdgeCacheOriginFlexShieldingOutputReference", jsii.get(self, "flexShielding"))

    @builtins.property
    @jsii.member(jsii_name="originOverrideAction")
    def origin_override_action(
        self,
    ) -> "NetworkServicesEdgeCacheOriginOriginOverrideActionOutputReference":
        return typing.cast("NetworkServicesEdgeCacheOriginOriginOverrideActionOutputReference", jsii.get(self, "originOverrideAction"))

    @builtins.property
    @jsii.member(jsii_name="originRedirect")
    def origin_redirect(
        self,
    ) -> "NetworkServicesEdgeCacheOriginOriginRedirectOutputReference":
        return typing.cast("NetworkServicesEdgeCacheOriginOriginRedirectOutputReference", jsii.get(self, "originRedirect"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> "NetworkServicesEdgeCacheOriginTimeoutOutputReference":
        return typing.cast("NetworkServicesEdgeCacheOriginTimeoutOutputReference", jsii.get(self, "timeout"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkServicesEdgeCacheOriginTimeoutsOutputReference":
        return typing.cast("NetworkServicesEdgeCacheOriginTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="awsV4AuthenticationInput")
    def aws_v4_authentication_input(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheOriginAwsV4Authentication"]:
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheOriginAwsV4Authentication"], jsii.get(self, "awsV4AuthenticationInput"))

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
    ) -> typing.Optional["NetworkServicesEdgeCacheOriginFlexShielding"]:
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheOriginFlexShielding"], jsii.get(self, "flexShieldingInput"))

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
    ) -> typing.Optional["NetworkServicesEdgeCacheOriginOriginOverrideAction"]:
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheOriginOriginOverrideAction"], jsii.get(self, "originOverrideActionInput"))

    @builtins.property
    @jsii.member(jsii_name="originRedirectInput")
    def origin_redirect_input(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheOriginOriginRedirect"]:
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheOriginOriginRedirect"], jsii.get(self, "originRedirectInput"))

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
    def timeout_input(self) -> typing.Optional["NetworkServicesEdgeCacheOriginTimeout"]:
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheOriginTimeout"], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkServicesEdgeCacheOriginTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkServicesEdgeCacheOriginTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e06de5d4511b597377b3704165fe68f5061fa218cccc1fb02c78010c20bf3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failoverOrigin")
    def failover_origin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failoverOrigin"))

    @failover_origin.setter
    def failover_origin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bed1df947dd4291ac8d920c17d244da333aaa0d36e1cd8e7fe3d8f7e2c2e443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverOrigin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57018818f7b0afffe196d835a8c51a510d6b467bbcacea6d00c751113523eabb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0283f28f9e9bc54b93c31c6b3ec148410010935ab9e8d028e90813f452c84eac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAttempts")
    def max_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAttempts"))

    @max_attempts.setter
    def max_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad6d4a66a9d05fab3c121584245b9c9f96fa5994855897ff30712f56c79364c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed9fada3a5871a695333a3deadef144f6f9fff05eadb9bd6de1f45bfea3c42f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originAddress")
    def origin_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originAddress"))

    @origin_address.setter
    def origin_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23fb04baf13d9e0a5b80c4e50b72113920ec1e68b117ebac295889879b98f31a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62b94ae140109467add0660268aebaa3f483b49534e665c01fa0682bac8272a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b1d456352eea565e3617e50b7f26ff00fc89c44a4967c2b1ca8771063e722bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d22aadbd696b95d5f31e42cd11056a698b7c1a2be7aa5d482a4c3c389e5aa4ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryConditions")
    def retry_conditions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "retryConditions"))

    @retry_conditions.setter
    def retry_conditions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__137537043a957722109451292d236f6c95d403fc6d78efe856a78937f37eb7f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryConditions", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginAwsV4Authentication",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id": "accessKeyId",
        "origin_region": "originRegion",
        "secret_access_key_version": "secretAccessKeyVersion",
    },
)
class NetworkServicesEdgeCacheOriginAwsV4Authentication:
    def __init__(
        self,
        *,
        access_key_id: builtins.str,
        origin_region: builtins.str,
        secret_access_key_version: builtins.str,
    ) -> None:
        '''
        :param access_key_id: The access key ID your origin uses to identify the key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#access_key_id NetworkServicesEdgeCacheOrigin#access_key_id}
        :param origin_region: The name of the AWS region that your origin is in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#origin_region NetworkServicesEdgeCacheOrigin#origin_region}
        :param secret_access_key_version: The Secret Manager secret version of the secret access key used by your origin. This is the resource name of the secret version in the format 'projects/* /secrets/* /versions/*' where the '*' values are replaced by the project, secret, and version you require. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#secret_access_key_version NetworkServicesEdgeCacheOrigin#secret_access_key_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66e5dec465d5b7635b95bef1883417915cba4c6b65ca53f5dab11b22ce9f43dc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#access_key_id NetworkServicesEdgeCacheOrigin#access_key_id}
        '''
        result = self._values.get("access_key_id")
        assert result is not None, "Required property 'access_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin_region(self) -> builtins.str:
        '''The name of the AWS region that your origin is in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#origin_region NetworkServicesEdgeCacheOrigin#origin_region}
        '''
        result = self._values.get("origin_region")
        assert result is not None, "Required property 'origin_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_access_key_version(self) -> builtins.str:
        '''The Secret Manager secret version of the secret access key used by your origin.

        This is the resource name of the secret version in the format 'projects/* /secrets/* /versions/*' where the '*' values are replaced by the project, secret, and version you require.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#secret_access_key_version NetworkServicesEdgeCacheOrigin#secret_access_key_version}

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
        return "NetworkServicesEdgeCacheOriginAwsV4Authentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheOriginAwsV4AuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginAwsV4AuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7df46e97393357f5d549387189e1c1e2601aef30432c247cee4b4ef8afc51d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e13308eaf0c2d1b431afc017b8b117cefa10371ff0948b3aba53fa557c6249d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originRegion")
    def origin_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originRegion"))

    @origin_region.setter
    def origin_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0de7c6e7fa5cc74b17059bbb124a783198213a80fbb46b2342c097bb221cea16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyVersion")
    def secret_access_key_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretAccessKeyVersion"))

    @secret_access_key_version.setter
    def secret_access_key_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbc1b5db3b3356a02bc8a4105ebaf2857f11014ee5add98a59ecf142604dc1c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKeyVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheOriginAwsV4Authentication]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheOriginAwsV4Authentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheOriginAwsV4Authentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc3c1ceaa95f0faa9de888c1318870524750a47e45003ce11b381cbe049bc87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginConfig",
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
class NetworkServicesEdgeCacheOriginConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        aws_v4_authentication: typing.Optional[typing.Union[NetworkServicesEdgeCacheOriginAwsV4Authentication, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        failover_origin: typing.Optional[builtins.str] = None,
        flex_shielding: typing.Optional[typing.Union["NetworkServicesEdgeCacheOriginFlexShielding", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_attempts: typing.Optional[jsii.Number] = None,
        origin_override_action: typing.Optional[typing.Union["NetworkServicesEdgeCacheOriginOriginOverrideAction", typing.Dict[builtins.str, typing.Any]]] = None,
        origin_redirect: typing.Optional[typing.Union["NetworkServicesEdgeCacheOriginOriginRedirect", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout: typing.Optional[typing.Union["NetworkServicesEdgeCacheOriginTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["NetworkServicesEdgeCacheOriginTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#name NetworkServicesEdgeCacheOrigin#name}
        :param origin_address: A fully qualified domain name (FQDN) or IP address reachable over the public Internet, or the address of a Google Cloud Storage bucket. This address will be used as the origin for cache requests - e.g. FQDN: media-backend.example.com, IPv4: 35.218.1.1, IPv6: 2607:f8b0:4012:809::200e, Cloud Storage: gs://bucketname When providing an FQDN (hostname), it must be publicly resolvable (e.g. via Google public DNS) and IP addresses must be publicly routable. It must not contain a protocol (e.g., https://) and it must not contain any slashes. If a Cloud Storage bucket is provided, it must be in the canonical "gs://bucketname" format. Other forms, such as "storage.googleapis.com", will be rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#origin_address NetworkServicesEdgeCacheOrigin#origin_address}
        :param aws_v4_authentication: aws_v4_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#aws_v4_authentication NetworkServicesEdgeCacheOrigin#aws_v4_authentication}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#description NetworkServicesEdgeCacheOrigin#description}
        :param failover_origin: The Origin resource to try when the current origin cannot be reached. After maxAttempts is reached, the configured failoverOrigin will be used to fulfil the request. The value of timeout.maxAttemptsTimeout dictates the timeout across all origins. A reference to a Topic resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#failover_origin NetworkServicesEdgeCacheOrigin#failover_origin}
        :param flex_shielding: flex_shielding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#flex_shielding NetworkServicesEdgeCacheOrigin#flex_shielding}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#id NetworkServicesEdgeCacheOrigin#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the EdgeCache resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#labels NetworkServicesEdgeCacheOrigin#labels}
        :param max_attempts: The maximum number of attempts to cache fill from this origin. Another attempt is made when a cache fill fails with one of the retryConditions. Once maxAttempts to this origin have failed the failoverOrigin will be used, if one is specified. That failoverOrigin may specify its own maxAttempts, retryConditions and failoverOrigin to control its own cache fill failures. The total number of allowed attempts to cache fill across this and failover origins is limited to four. The total time allowed for cache fill attempts across this and failover origins can be controlled with maxAttemptsTimeout. The last valid, non-retried response from all origins will be returned to the client. If no origin returns a valid response, an HTTP 502 will be returned to the client. Defaults to 1. Must be a value greater than 0 and less than 4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#max_attempts NetworkServicesEdgeCacheOrigin#max_attempts}
        :param origin_override_action: origin_override_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#origin_override_action NetworkServicesEdgeCacheOrigin#origin_override_action}
        :param origin_redirect: origin_redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#origin_redirect NetworkServicesEdgeCacheOrigin#origin_redirect}
        :param port: The port to connect to the origin on. Defaults to port 443 for HTTP2 and HTTPS protocols, and port 80 for HTTP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#port NetworkServicesEdgeCacheOrigin#port}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#project NetworkServicesEdgeCacheOrigin#project}.
        :param protocol: The protocol to use to connect to the configured origin. Defaults to HTTP2, and it is strongly recommended that users use HTTP2 for both security & performance. When using HTTP2 or HTTPS as the protocol, a valid, publicly-signed, unexpired TLS (SSL) certificate must be presented by the origin server. Possible values: ["HTTP2", "HTTPS", "HTTP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#protocol NetworkServicesEdgeCacheOrigin#protocol}
        :param retry_conditions: Specifies one or more retry conditions for the configured origin. If the failure mode during a connection attempt to the origin matches the configured retryCondition(s), the origin request will be retried up to maxAttempts times. The failoverOrigin, if configured, will then be used to satisfy the request. The default retryCondition is "CONNECT_FAILURE". retryConditions apply to this origin, and not subsequent failoverOrigin(s), which may specify their own retryConditions and maxAttempts. Valid values are: - CONNECT_FAILURE: Retry on failures connecting to origins, for example due to connection timeouts. - HTTP_5XX: Retry if the origin responds with any 5xx response code, or if the origin does not respond at all, example: disconnects, reset, read timeout, connection failure, and refused streams. - GATEWAY_ERROR: Similar to 5xx, but only applies to response codes 502, 503 or 504. - RETRIABLE_4XX: Retry for retriable 4xx response codes, which include HTTP 409 (Conflict) and HTTP 429 (Too Many Requests) - NOT_FOUND: Retry if the origin returns a HTTP 404 (Not Found). This can be useful when generating video content, and the segment is not available yet. - FORBIDDEN: Retry if the origin returns a HTTP 403 (Forbidden). Possible values: ["CONNECT_FAILURE", "HTTP_5XX", "GATEWAY_ERROR", "RETRIABLE_4XX", "NOT_FOUND", "FORBIDDEN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#retry_conditions NetworkServicesEdgeCacheOrigin#retry_conditions}
        :param timeout: timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#timeout NetworkServicesEdgeCacheOrigin#timeout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#timeouts NetworkServicesEdgeCacheOrigin#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(aws_v4_authentication, dict):
            aws_v4_authentication = NetworkServicesEdgeCacheOriginAwsV4Authentication(**aws_v4_authentication)
        if isinstance(flex_shielding, dict):
            flex_shielding = NetworkServicesEdgeCacheOriginFlexShielding(**flex_shielding)
        if isinstance(origin_override_action, dict):
            origin_override_action = NetworkServicesEdgeCacheOriginOriginOverrideAction(**origin_override_action)
        if isinstance(origin_redirect, dict):
            origin_redirect = NetworkServicesEdgeCacheOriginOriginRedirect(**origin_redirect)
        if isinstance(timeout, dict):
            timeout = NetworkServicesEdgeCacheOriginTimeout(**timeout)
        if isinstance(timeouts, dict):
            timeouts = NetworkServicesEdgeCacheOriginTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dcb37a20d2a8ad5c4e32b9ddaab86c1be8a7fe650e95e7e38db09255ea5c30c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#name NetworkServicesEdgeCacheOrigin#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#origin_address NetworkServicesEdgeCacheOrigin#origin_address}
        '''
        result = self._values.get("origin_address")
        assert result is not None, "Required property 'origin_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_v4_authentication(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheOriginAwsV4Authentication]:
        '''aws_v4_authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#aws_v4_authentication NetworkServicesEdgeCacheOrigin#aws_v4_authentication}
        '''
        result = self._values.get("aws_v4_authentication")
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheOriginAwsV4Authentication], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#description NetworkServicesEdgeCacheOrigin#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failover_origin(self) -> typing.Optional[builtins.str]:
        '''The Origin resource to try when the current origin cannot be reached.

        After maxAttempts is reached, the configured failoverOrigin will be used to fulfil the request.

        The value of timeout.maxAttemptsTimeout dictates the timeout across all origins.
        A reference to a Topic resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#failover_origin NetworkServicesEdgeCacheOrigin#failover_origin}
        '''
        result = self._values.get("failover_origin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flex_shielding(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheOriginFlexShielding"]:
        '''flex_shielding block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#flex_shielding NetworkServicesEdgeCacheOrigin#flex_shielding}
        '''
        result = self._values.get("flex_shielding")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheOriginFlexShielding"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#id NetworkServicesEdgeCacheOrigin#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#labels NetworkServicesEdgeCacheOrigin#labels}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#max_attempts NetworkServicesEdgeCacheOrigin#max_attempts}
        '''
        result = self._values.get("max_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def origin_override_action(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheOriginOriginOverrideAction"]:
        '''origin_override_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#origin_override_action NetworkServicesEdgeCacheOrigin#origin_override_action}
        '''
        result = self._values.get("origin_override_action")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheOriginOriginOverrideAction"], result)

    @builtins.property
    def origin_redirect(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheOriginOriginRedirect"]:
        '''origin_redirect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#origin_redirect NetworkServicesEdgeCacheOrigin#origin_redirect}
        '''
        result = self._values.get("origin_redirect")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheOriginOriginRedirect"], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port to connect to the origin on.

        Defaults to port 443 for HTTP2 and HTTPS protocols, and port 80 for HTTP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#port NetworkServicesEdgeCacheOrigin#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#project NetworkServicesEdgeCacheOrigin#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol to use to connect to the configured origin.

        Defaults to HTTP2, and it is strongly recommended that users use HTTP2 for both security & performance.

        When using HTTP2 or HTTPS as the protocol, a valid, publicly-signed, unexpired TLS (SSL) certificate must be presented by the origin server. Possible values: ["HTTP2", "HTTPS", "HTTP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#protocol NetworkServicesEdgeCacheOrigin#protocol}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#retry_conditions NetworkServicesEdgeCacheOrigin#retry_conditions}
        '''
        result = self._values.get("retry_conditions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional["NetworkServicesEdgeCacheOriginTimeout"]:
        '''timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#timeout NetworkServicesEdgeCacheOrigin#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheOriginTimeout"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkServicesEdgeCacheOriginTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#timeouts NetworkServicesEdgeCacheOrigin#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheOriginTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheOriginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginFlexShielding",
    jsii_struct_bases=[],
    name_mapping={"flex_shielding_regions": "flexShieldingRegions"},
)
class NetworkServicesEdgeCacheOriginFlexShielding:
    def __init__(
        self,
        *,
        flex_shielding_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param flex_shielding_regions: Whenever possible, content will be fetched from origin and cached in or near the specified origin. Best effort. You must specify exactly one FlexShieldingRegion. Possible values: ["AFRICA_SOUTH1", "ME_CENTRAL1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#flex_shielding_regions NetworkServicesEdgeCacheOrigin#flex_shielding_regions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4987843609fd88fdce35f28aeacfada65926be10d7c6af438c5bef1adb0346)
            check_type(argname="argument flex_shielding_regions", value=flex_shielding_regions, expected_type=type_hints["flex_shielding_regions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if flex_shielding_regions is not None:
            self._values["flex_shielding_regions"] = flex_shielding_regions

    @builtins.property
    def flex_shielding_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Whenever possible, content will be fetched from origin and cached in or near the specified origin. Best effort.

        You must specify exactly one FlexShieldingRegion. Possible values: ["AFRICA_SOUTH1", "ME_CENTRAL1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#flex_shielding_regions NetworkServicesEdgeCacheOrigin#flex_shielding_regions}
        '''
        result = self._values.get("flex_shielding_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheOriginFlexShielding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheOriginFlexShieldingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginFlexShieldingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31f435bb1e085f43bdb430081803365d92f82697d5306c8c4e7afc44755ec3c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__502df7d0d35fb24055853de1302fab92f912eea81c8446d76ce6d8c6d57aa8b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flexShieldingRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheOriginFlexShielding]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheOriginFlexShielding], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheOriginFlexShielding],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__418ca7d023c0ed5edcba5ebc37534412c5d02eae3e0ff45d0f710d207b5710a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginOriginOverrideAction",
    jsii_struct_bases=[],
    name_mapping={"header_action": "headerAction", "url_rewrite": "urlRewrite"},
)
class NetworkServicesEdgeCacheOriginOriginOverrideAction:
    def __init__(
        self,
        *,
        header_action: typing.Optional[typing.Union["NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction", typing.Dict[builtins.str, typing.Any]]] = None,
        url_rewrite: typing.Optional[typing.Union["NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param header_action: header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#header_action NetworkServicesEdgeCacheOrigin#header_action}
        :param url_rewrite: url_rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#url_rewrite NetworkServicesEdgeCacheOrigin#url_rewrite}
        '''
        if isinstance(header_action, dict):
            header_action = NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction(**header_action)
        if isinstance(url_rewrite, dict):
            url_rewrite = NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite(**url_rewrite)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0d0afad0e304117066613ce46ce4a6237328e5c62da21fbdea3720ea01c719)
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
    ) -> typing.Optional["NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction"]:
        '''header_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#header_action NetworkServicesEdgeCacheOrigin#header_action}
        '''
        result = self._values.get("header_action")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction"], result)

    @builtins.property
    def url_rewrite(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite"]:
        '''url_rewrite block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#url_rewrite NetworkServicesEdgeCacheOrigin#url_rewrite}
        '''
        result = self._values.get("url_rewrite")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheOriginOriginOverrideAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction",
    jsii_struct_bases=[],
    name_mapping={"request_headers_to_add": "requestHeadersToAdd"},
)
class NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction:
    def __init__(
        self,
        *,
        request_headers_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param request_headers_to_add: request_headers_to_add block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#request_headers_to_add NetworkServicesEdgeCacheOrigin#request_headers_to_add}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb5747c5f9f745a5b84935c0332daf56719f5eab6264e1979100b8531f68344d)
            check_type(argname="argument request_headers_to_add", value=request_headers_to_add, expected_type=type_hints["request_headers_to_add"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if request_headers_to_add is not None:
            self._values["request_headers_to_add"] = request_headers_to_add

    @builtins.property
    def request_headers_to_add(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd"]]]:
        '''request_headers_to_add block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#request_headers_to_add NetworkServicesEdgeCacheOrigin#request_headers_to_add}
        '''
        result = self._values.get("request_headers_to_add")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__235386b58e782df33a025632935c4c5bae625e1bc253787c90473265d5356a88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequestHeadersToAdd")
    def put_request_headers_to_add(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3b7227c4d0f517d0238414f5823e435927a748ef99e8944d99119dff60dc12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeadersToAdd", [value]))

    @jsii.member(jsii_name="resetRequestHeadersToAdd")
    def reset_request_headers_to_add(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeadersToAdd", []))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersToAdd")
    def request_headers_to_add(
        self,
    ) -> "NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddList":
        return typing.cast("NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddList", jsii.get(self, "requestHeadersToAdd"))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersToAddInput")
    def request_headers_to_add_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd"]]], jsii.get(self, "requestHeadersToAddInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f579e40cb4559d1ff61c59831cce922a7e8082702dce5ae8ab46c8ff5cf11a72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd",
    jsii_struct_bases=[],
    name_mapping={
        "header_name": "headerName",
        "header_value": "headerValue",
        "replace": "replace",
    },
)
class NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        header_value: builtins.str,
        replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param header_name: The name of the header to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#header_name NetworkServicesEdgeCacheOrigin#header_name}
        :param header_value: The value of the header to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#header_value NetworkServicesEdgeCacheOrigin#header_value}
        :param replace: Whether to replace all existing headers with the same name. By default, added header values are appended to the response or request headers with the same field names. The added values are separated by commas. To overwrite existing values, set 'replace' to 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#replace NetworkServicesEdgeCacheOrigin#replace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a73296c76bf227ddb25ad7868d17abe3bd7bdf61cb3314096aa63b2c9b34280)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#header_name NetworkServicesEdgeCacheOrigin#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header_value(self) -> builtins.str:
        '''The value of the header to add.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#header_value NetworkServicesEdgeCacheOrigin#header_value}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#replace NetworkServicesEdgeCacheOrigin#replace}
        '''
        result = self._values.get("replace")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__deb72765bdea71bb63a3b487ac105144cedbb6c0ecbb6b8c54d100dd0fab5126)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ef32a25359a5c60797b6f010a4cbafa76fec2311f4761011dbd3447411db98)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91cd3527126655068326605b269a638fa86f83efcac698d01ba03813bf842a48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2a1cef96f2cdbe6ce574c4e1771b86f4541754a533a08690ab40da59cbe2810)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91eb585aae9787356037ec3f43f50d13bb49b50c967668ee096f79aa179bf00d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b86f65c31c8c410ec93c0121969507c0f3ad2c236b76185b14b570cb1561edbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbd0f67099123f2c4b5fbf81f4fa8a1a08337c957c2095fad1e2a81a4561c826)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afdddf11a2465c16eb87f3bcc220672a2450b1ab81c412768afef33f1cb5c3bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))

    @header_value.setter
    def header_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da2ac1a51facf374e6a8ada62d892cf32f13b38ec5ea9e13cf0eb345d0df8f03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26591cdd96f299d6afc54c1fb247e0cd61501e39723ad125ee7d2bdc044a4141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd6771edf4b3af2c297081bfa5231ef8f8808cced58863ddbe8be7862640db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheOriginOriginOverrideActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginOriginOverrideActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d46f17cb53b5ac8e850162d0a1905e86b19d34cf3d6b0e9bb28ae83bfa5b465e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaderAction")
    def put_header_action(
        self,
        *,
        request_headers_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param request_headers_to_add: request_headers_to_add block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#request_headers_to_add NetworkServicesEdgeCacheOrigin#request_headers_to_add}
        '''
        value = NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction(
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
        :param host_rewrite: Prior to forwarding the request to the selected origin, the request's host header is replaced with contents of the hostRewrite. This value must be between 1 and 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#host_rewrite NetworkServicesEdgeCacheOrigin#host_rewrite}
        '''
        value = NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite(
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
    ) -> NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionOutputReference:
        return typing.cast(NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionOutputReference, jsii.get(self, "headerAction"))

    @builtins.property
    @jsii.member(jsii_name="urlRewrite")
    def url_rewrite(
        self,
    ) -> "NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewriteOutputReference":
        return typing.cast("NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewriteOutputReference", jsii.get(self, "urlRewrite"))

    @builtins.property
    @jsii.member(jsii_name="headerActionInput")
    def header_action_input(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction], jsii.get(self, "headerActionInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRewriteInput")
    def url_rewrite_input(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite"]:
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite"], jsii.get(self, "urlRewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheOriginOriginOverrideAction]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheOriginOriginOverrideAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheOriginOriginOverrideAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d1a60a10fc83525c0cac6cdd75136ba661d13e57611b9b0fa270e5c4d9abd1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite",
    jsii_struct_bases=[],
    name_mapping={"host_rewrite": "hostRewrite"},
)
class NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite:
    def __init__(self, *, host_rewrite: typing.Optional[builtins.str] = None) -> None:
        '''
        :param host_rewrite: Prior to forwarding the request to the selected origin, the request's host header is replaced with contents of the hostRewrite. This value must be between 1 and 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#host_rewrite NetworkServicesEdgeCacheOrigin#host_rewrite}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__647303990ca330fb8b1a7809c4961bfe3264c70e6e46b65b33b30709c69527b4)
            check_type(argname="argument host_rewrite", value=host_rewrite, expected_type=type_hints["host_rewrite"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host_rewrite is not None:
            self._values["host_rewrite"] = host_rewrite

    @builtins.property
    def host_rewrite(self) -> typing.Optional[builtins.str]:
        '''Prior to forwarding the request to the selected origin, the request's host header is replaced with contents of the hostRewrite.

        This value must be between 1 and 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#host_rewrite NetworkServicesEdgeCacheOrigin#host_rewrite}
        '''
        result = self._values.get("host_rewrite")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewriteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewriteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20d0ab8a2d18c9295c915bc635b29ce30564e4235d6addb2d6b7582b67481989)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97f731058689a7cb2482a859da0f3f8b2fc3815ccc2e528e5c69170c1c9112a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostRewrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306115db3fa75ccb57349601a01b4a8c49f47345dcbb7085d16ceba3cf6a02f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginOriginRedirect",
    jsii_struct_bases=[],
    name_mapping={"redirect_conditions": "redirectConditions"},
)
class NetworkServicesEdgeCacheOriginOriginRedirect:
    def __init__(
        self,
        *,
        redirect_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param redirect_conditions: The set of redirect response codes that the CDN follows. Values of `RedirectConditions <https://cloud.google.com/media-cdn/docs/reference/rest/v1/projects.locations.edgeCacheOrigins#redirectconditions>`_ are accepted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#redirect_conditions NetworkServicesEdgeCacheOrigin#redirect_conditions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c059a8055bef1271b39d0ee21e0f3d3758360ee955cf052ab597392293f644)
            check_type(argname="argument redirect_conditions", value=redirect_conditions, expected_type=type_hints["redirect_conditions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if redirect_conditions is not None:
            self._values["redirect_conditions"] = redirect_conditions

    @builtins.property
    def redirect_conditions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of redirect response codes that the CDN follows. Values of `RedirectConditions <https://cloud.google.com/media-cdn/docs/reference/rest/v1/projects.locations.edgeCacheOrigins#redirectconditions>`_ are accepted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#redirect_conditions NetworkServicesEdgeCacheOrigin#redirect_conditions}
        '''
        result = self._values.get("redirect_conditions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheOriginOriginRedirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheOriginOriginRedirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginOriginRedirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92911f5cb0b82ffb4f440dca9fff88863cbe37d4fbdf1a13a115108cceedfaf5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74e3d1f8af6e31162d626e148c279f89df870a99c0bc797bce50dcc199a829b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectConditions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheOriginOriginRedirect]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheOriginOriginRedirect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheOriginOriginRedirect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__459db954b54e5f253f2faca8bbfed98008ddb6af35a8793db9ed01636c9a5972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginTimeout",
    jsii_struct_bases=[],
    name_mapping={
        "connect_timeout": "connectTimeout",
        "max_attempts_timeout": "maxAttemptsTimeout",
        "read_timeout": "readTimeout",
        "response_timeout": "responseTimeout",
    },
)
class NetworkServicesEdgeCacheOriginTimeout:
    def __init__(
        self,
        *,
        connect_timeout: typing.Optional[builtins.str] = None,
        max_attempts_timeout: typing.Optional[builtins.str] = None,
        read_timeout: typing.Optional[builtins.str] = None,
        response_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connect_timeout: The maximum duration to wait for a single origin connection to be established, including DNS lookup, TLS handshake and TCP/QUIC connection establishment. Defaults to 5 seconds. The timeout must be a value between 1s and 15s. The connectTimeout capped by the deadline set by the request's maxAttemptsTimeout. The last connection attempt may have a smaller connectTimeout in order to adhere to the overall maxAttemptsTimeout. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#connect_timeout NetworkServicesEdgeCacheOrigin#connect_timeout}
        :param max_attempts_timeout: The maximum time across all connection attempts to the origin, including failover origins, before returning an error to the client. A HTTP 504 will be returned if the timeout is reached before a response is returned. Defaults to 15 seconds. The timeout must be a value between 1s and 30s. If a failoverOrigin is specified, the maxAttemptsTimeout of the first configured origin sets the deadline for all connection attempts across all failoverOrigins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#max_attempts_timeout NetworkServicesEdgeCacheOrigin#max_attempts_timeout}
        :param read_timeout: The maximum duration to wait between reads of a single HTTP connection/stream. Defaults to 15 seconds. The timeout must be a value between 1s and 30s. The readTimeout is capped by the responseTimeout. All reads of the HTTP connection/stream must be completed by the deadline set by the responseTimeout. If the response headers have already been written to the connection, the response will be truncated and logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#read_timeout NetworkServicesEdgeCacheOrigin#read_timeout}
        :param response_timeout: The maximum duration to wait for the last byte of a response to arrive when reading from the HTTP connection/stream. Defaults to 30 seconds. The timeout must be a value between 1s and 120s. The responseTimeout starts after the connection has been established. This also applies to HTTP Chunked Transfer Encoding responses, and/or when an open-ended Range request is made to the origin. Origins that take longer to write additional bytes to the response than the configured responseTimeout will result in an error being returned to the client. If the response headers have already been written to the connection, the response will be truncated and logged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#response_timeout NetworkServicesEdgeCacheOrigin#response_timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e8085f0f540c26a6d6478e628a51dd6039cd1193b8968b27bf1ee6546a2416)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#connect_timeout NetworkServicesEdgeCacheOrigin#connect_timeout}
        '''
        result = self._values.get("connect_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_attempts_timeout(self) -> typing.Optional[builtins.str]:
        '''The maximum time across all connection attempts to the origin, including failover origins, before returning an error to the client.

        A HTTP 504 will be returned if the timeout is reached before a response is returned.

        Defaults to 15 seconds. The timeout must be a value between 1s and 30s.

        If a failoverOrigin is specified, the maxAttemptsTimeout of the first configured origin sets the deadline for all connection attempts across all failoverOrigins.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#max_attempts_timeout NetworkServicesEdgeCacheOrigin#max_attempts_timeout}
        '''
        result = self._values.get("max_attempts_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_timeout(self) -> typing.Optional[builtins.str]:
        '''The maximum duration to wait between reads of a single HTTP connection/stream.

        Defaults to 15 seconds.  The timeout must be a value between 1s and 30s.

        The readTimeout is capped by the responseTimeout.  All reads of the HTTP connection/stream must be completed by the deadline set by the responseTimeout.

        If the response headers have already been written to the connection, the response will be truncated and logged.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#read_timeout NetworkServicesEdgeCacheOrigin#read_timeout}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#response_timeout NetworkServicesEdgeCacheOrigin#response_timeout}
        '''
        result = self._values.get("response_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheOriginTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheOriginTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a93469c1f5102e842415c30010ae3830e3e0232f2e64bdc6a718418f645ba951)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42f9b1ca47700c1923a17cea1159b5a774b83a307fe5cfb52be6059d7b6672a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAttemptsTimeout")
    def max_attempts_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxAttemptsTimeout"))

    @max_attempts_timeout.setter
    def max_attempts_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d080edf18cfb051fb64ef435466dc4208303dd701f22675116db8dda763db54f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAttemptsTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readTimeout")
    def read_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readTimeout"))

    @read_timeout.setter
    def read_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e81b4afb74cb177142b84e004ecad625d1a8820162c5ac9a3a227fd905fe5148)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseTimeout")
    def response_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseTimeout"))

    @response_timeout.setter
    def response_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc54da3751259c20044434da499f369fc836c5e1e062382372ae9ff2dd364903)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetworkServicesEdgeCacheOriginTimeout]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheOriginTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheOriginTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__accdefea2feb68dfd48bf58c7de1ff4ab766047bad40e7dc6f1ddb9c52d31839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkServicesEdgeCacheOriginTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#create NetworkServicesEdgeCacheOrigin#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#delete NetworkServicesEdgeCacheOrigin#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#update NetworkServicesEdgeCacheOrigin#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48290cbe5d8d7bb5e130b0ee838e2e5e5f2bbd0e3c5fcc00c118deaa4c128bef)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#create NetworkServicesEdgeCacheOrigin#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#delete NetworkServicesEdgeCacheOrigin#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_origin#update NetworkServicesEdgeCacheOrigin#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheOriginTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheOriginTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheOrigin.NetworkServicesEdgeCacheOriginTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68d030eb456d40ae00e9264aa84cf010c0702327d48eeb3983fc76f3bf986d18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91d06d40a306e38f336fa5e90378ccab47a1187e9be4c3f1f676c16d0be2a94e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f9e7912fe33ecb192bda4b6beebcd3c045a5f6e320d01e68d1f0686764c2b98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0256e91321e29295953d4f1d4448bc08ecd286933fbdf4b825dd93799c5d973e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheOriginTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheOriginTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheOriginTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be178a4410c910600d40f1129dfc841e6e28ef1bdeac5328b1f347e0d0ea57c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkServicesEdgeCacheOrigin",
    "NetworkServicesEdgeCacheOriginAwsV4Authentication",
    "NetworkServicesEdgeCacheOriginAwsV4AuthenticationOutputReference",
    "NetworkServicesEdgeCacheOriginConfig",
    "NetworkServicesEdgeCacheOriginFlexShielding",
    "NetworkServicesEdgeCacheOriginFlexShieldingOutputReference",
    "NetworkServicesEdgeCacheOriginOriginOverrideAction",
    "NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction",
    "NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionOutputReference",
    "NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd",
    "NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddList",
    "NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAddOutputReference",
    "NetworkServicesEdgeCacheOriginOriginOverrideActionOutputReference",
    "NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite",
    "NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewriteOutputReference",
    "NetworkServicesEdgeCacheOriginOriginRedirect",
    "NetworkServicesEdgeCacheOriginOriginRedirectOutputReference",
    "NetworkServicesEdgeCacheOriginTimeout",
    "NetworkServicesEdgeCacheOriginTimeoutOutputReference",
    "NetworkServicesEdgeCacheOriginTimeouts",
    "NetworkServicesEdgeCacheOriginTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c1c21df93d1996318f9c957070740c8d72e22c37e5bff3072eb29fb680a72cb2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    origin_address: builtins.str,
    aws_v4_authentication: typing.Optional[typing.Union[NetworkServicesEdgeCacheOriginAwsV4Authentication, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    failover_origin: typing.Optional[builtins.str] = None,
    flex_shielding: typing.Optional[typing.Union[NetworkServicesEdgeCacheOriginFlexShielding, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_attempts: typing.Optional[jsii.Number] = None,
    origin_override_action: typing.Optional[typing.Union[NetworkServicesEdgeCacheOriginOriginOverrideAction, typing.Dict[builtins.str, typing.Any]]] = None,
    origin_redirect: typing.Optional[typing.Union[NetworkServicesEdgeCacheOriginOriginRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeout: typing.Optional[typing.Union[NetworkServicesEdgeCacheOriginTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[NetworkServicesEdgeCacheOriginTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__1c0c9cb22d1d6da3c50e953c0b256bef0c7c9661ee5270c800c50c0c4d630f9f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e06de5d4511b597377b3704165fe68f5061fa218cccc1fb02c78010c20bf3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bed1df947dd4291ac8d920c17d244da333aaa0d36e1cd8e7fe3d8f7e2c2e443(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57018818f7b0afffe196d835a8c51a510d6b467bbcacea6d00c751113523eabb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0283f28f9e9bc54b93c31c6b3ec148410010935ab9e8d028e90813f452c84eac(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad6d4a66a9d05fab3c121584245b9c9f96fa5994855897ff30712f56c79364c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9fada3a5871a695333a3deadef144f6f9fff05eadb9bd6de1f45bfea3c42f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23fb04baf13d9e0a5b80c4e50b72113920ec1e68b117ebac295889879b98f31a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62b94ae140109467add0660268aebaa3f483b49534e665c01fa0682bac8272a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b1d456352eea565e3617e50b7f26ff00fc89c44a4967c2b1ca8771063e722bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d22aadbd696b95d5f31e42cd11056a698b7c1a2be7aa5d482a4c3c389e5aa4ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137537043a957722109451292d236f6c95d403fc6d78efe856a78937f37eb7f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e5dec465d5b7635b95bef1883417915cba4c6b65ca53f5dab11b22ce9f43dc(
    *,
    access_key_id: builtins.str,
    origin_region: builtins.str,
    secret_access_key_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7df46e97393357f5d549387189e1c1e2601aef30432c247cee4b4ef8afc51d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e13308eaf0c2d1b431afc017b8b117cefa10371ff0948b3aba53fa557c6249d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de7c6e7fa5cc74b17059bbb124a783198213a80fbb46b2342c097bb221cea16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc1b5db3b3356a02bc8a4105ebaf2857f11014ee5add98a59ecf142604dc1c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc3c1ceaa95f0faa9de888c1318870524750a47e45003ce11b381cbe049bc87(
    value: typing.Optional[NetworkServicesEdgeCacheOriginAwsV4Authentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dcb37a20d2a8ad5c4e32b9ddaab86c1be8a7fe650e95e7e38db09255ea5c30c(
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
    aws_v4_authentication: typing.Optional[typing.Union[NetworkServicesEdgeCacheOriginAwsV4Authentication, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    failover_origin: typing.Optional[builtins.str] = None,
    flex_shielding: typing.Optional[typing.Union[NetworkServicesEdgeCacheOriginFlexShielding, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_attempts: typing.Optional[jsii.Number] = None,
    origin_override_action: typing.Optional[typing.Union[NetworkServicesEdgeCacheOriginOriginOverrideAction, typing.Dict[builtins.str, typing.Any]]] = None,
    origin_redirect: typing.Optional[typing.Union[NetworkServicesEdgeCacheOriginOriginRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeout: typing.Optional[typing.Union[NetworkServicesEdgeCacheOriginTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[NetworkServicesEdgeCacheOriginTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4987843609fd88fdce35f28aeacfada65926be10d7c6af438c5bef1adb0346(
    *,
    flex_shielding_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f435bb1e085f43bdb430081803365d92f82697d5306c8c4e7afc44755ec3c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502df7d0d35fb24055853de1302fab92f912eea81c8446d76ce6d8c6d57aa8b9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418ca7d023c0ed5edcba5ebc37534412c5d02eae3e0ff45d0f710d207b5710a3(
    value: typing.Optional[NetworkServicesEdgeCacheOriginFlexShielding],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0d0afad0e304117066613ce46ce4a6237328e5c62da21fbdea3720ea01c719(
    *,
    header_action: typing.Optional[typing.Union[NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction, typing.Dict[builtins.str, typing.Any]]] = None,
    url_rewrite: typing.Optional[typing.Union[NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5747c5f9f745a5b84935c0332daf56719f5eab6264e1979100b8531f68344d(
    *,
    request_headers_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235386b58e782df33a025632935c4c5bae625e1bc253787c90473265d5356a88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3b7227c4d0f517d0238414f5823e435927a748ef99e8944d99119dff60dc12(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f579e40cb4559d1ff61c59831cce922a7e8082702dce5ae8ab46c8ff5cf11a72(
    value: typing.Optional[NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a73296c76bf227ddb25ad7868d17abe3bd7bdf61cb3314096aa63b2c9b34280(
    *,
    header_name: builtins.str,
    header_value: builtins.str,
    replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb72765bdea71bb63a3b487ac105144cedbb6c0ecbb6b8c54d100dd0fab5126(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ef32a25359a5c60797b6f010a4cbafa76fec2311f4761011dbd3447411db98(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91cd3527126655068326605b269a638fa86f83efcac698d01ba03813bf842a48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a1cef96f2cdbe6ce574c4e1771b86f4541754a533a08690ab40da59cbe2810(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91eb585aae9787356037ec3f43f50d13bb49b50c967668ee096f79aa179bf00d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86f65c31c8c410ec93c0121969507c0f3ad2c236b76185b14b570cb1561edbc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd0f67099123f2c4b5fbf81f4fa8a1a08337c957c2095fad1e2a81a4561c826(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afdddf11a2465c16eb87f3bcc220672a2450b1ab81c412768afef33f1cb5c3bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da2ac1a51facf374e6a8ada62d892cf32f13b38ec5ea9e13cf0eb345d0df8f03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26591cdd96f299d6afc54c1fb247e0cd61501e39723ad125ee7d2bdc044a4141(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd6771edf4b3af2c297081bfa5231ef8f8808cced58863ddbe8be7862640db1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheOriginOriginOverrideActionHeaderActionRequestHeadersToAdd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46f17cb53b5ac8e850162d0a1905e86b19d34cf3d6b0e9bb28ae83bfa5b465e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1a60a10fc83525c0cac6cdd75136ba661d13e57611b9b0fa270e5c4d9abd1c(
    value: typing.Optional[NetworkServicesEdgeCacheOriginOriginOverrideAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647303990ca330fb8b1a7809c4961bfe3264c70e6e46b65b33b30709c69527b4(
    *,
    host_rewrite: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d0ab8a2d18c9295c915bc635b29ce30564e4235d6addb2d6b7582b67481989(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f731058689a7cb2482a859da0f3f8b2fc3815ccc2e528e5c69170c1c9112a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306115db3fa75ccb57349601a01b4a8c49f47345dcbb7085d16ceba3cf6a02f7(
    value: typing.Optional[NetworkServicesEdgeCacheOriginOriginOverrideActionUrlRewrite],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c059a8055bef1271b39d0ee21e0f3d3758360ee955cf052ab597392293f644(
    *,
    redirect_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92911f5cb0b82ffb4f440dca9fff88863cbe37d4fbdf1a13a115108cceedfaf5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e3d1f8af6e31162d626e148c279f89df870a99c0bc797bce50dcc199a829b3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459db954b54e5f253f2faca8bbfed98008ddb6af35a8793db9ed01636c9a5972(
    value: typing.Optional[NetworkServicesEdgeCacheOriginOriginRedirect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e8085f0f540c26a6d6478e628a51dd6039cd1193b8968b27bf1ee6546a2416(
    *,
    connect_timeout: typing.Optional[builtins.str] = None,
    max_attempts_timeout: typing.Optional[builtins.str] = None,
    read_timeout: typing.Optional[builtins.str] = None,
    response_timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93469c1f5102e842415c30010ae3830e3e0232f2e64bdc6a718418f645ba951(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f9b1ca47700c1923a17cea1159b5a774b83a307fe5cfb52be6059d7b6672a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d080edf18cfb051fb64ef435466dc4208303dd701f22675116db8dda763db54f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81b4afb74cb177142b84e004ecad625d1a8820162c5ac9a3a227fd905fe5148(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc54da3751259c20044434da499f369fc836c5e1e062382372ae9ff2dd364903(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__accdefea2feb68dfd48bf58c7de1ff4ab766047bad40e7dc6f1ddb9c52d31839(
    value: typing.Optional[NetworkServicesEdgeCacheOriginTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48290cbe5d8d7bb5e130b0ee838e2e5e5f2bbd0e3c5fcc00c118deaa4c128bef(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d030eb456d40ae00e9264aa84cf010c0702327d48eeb3983fc76f3bf986d18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d06d40a306e38f336fa5e90378ccab47a1187e9be4c3f1f676c16d0be2a94e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9e7912fe33ecb192bda4b6beebcd3c045a5f6e320d01e68d1f0686764c2b98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0256e91321e29295953d4f1d4448bc08ecd286933fbdf4b825dd93799c5d973e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be178a4410c910600d40f1129dfc841e6e28ef1bdeac5328b1f347e0d0ea57c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheOriginTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
