r'''
# `google_compute_backend_bucket`

Refer to the Terraform Registry for docs: [`google_compute_backend_bucket`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket).
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


class ComputeBackendBucket(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendBucket.ComputeBackendBucket",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket google_compute_backend_bucket}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bucket_name: builtins.str,
        name: builtins.str,
        cdn_policy: typing.Optional[typing.Union["ComputeBackendBucketCdnPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        compression_mode: typing.Optional[builtins.str] = None,
        custom_response_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        edge_security_policy: typing.Optional[builtins.str] = None,
        enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeBackendBucketTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket google_compute_backend_bucket} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bucket_name: Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#bucket_name ComputeBackendBucket#bucket_name}
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#name ComputeBackendBucket#name}
        :param cdn_policy: cdn_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#cdn_policy ComputeBackendBucket#cdn_policy}
        :param compression_mode: Compress text responses using Brotli or gzip compression, based on the client's Accept-Encoding header. Possible values: ["AUTOMATIC", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#compression_mode ComputeBackendBucket#compression_mode}
        :param custom_response_headers: Headers that the HTTP/S load balancer should add to proxied responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#custom_response_headers ComputeBackendBucket#custom_response_headers}
        :param description: An optional textual description of the resource; provided by the client when the resource is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#description ComputeBackendBucket#description}
        :param edge_security_policy: The security policy associated with this backend bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#edge_security_policy ComputeBackendBucket#edge_security_policy}
        :param enable_cdn: If true, enable Cloud CDN for this BackendBucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#enable_cdn ComputeBackendBucket#enable_cdn}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#id ComputeBackendBucket#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancing_scheme: The value can only be INTERNAL_MANAGED for cross-region internal layer 7 load balancer. If loadBalancingScheme is not specified, the backend bucket can be used by classic global external load balancers, or global application external load balancers, or both. Possible values: ["INTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#load_balancing_scheme ComputeBackendBucket#load_balancing_scheme}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#project ComputeBackendBucket#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#timeouts ComputeBackendBucket#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db11dd1506b3cd7bdf702512c2e7addc31839c7f7c93549dc6959e22849f3dda)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeBackendBucketConfig(
            bucket_name=bucket_name,
            name=name,
            cdn_policy=cdn_policy,
            compression_mode=compression_mode,
            custom_response_headers=custom_response_headers,
            description=description,
            edge_security_policy=edge_security_policy,
            enable_cdn=enable_cdn,
            id=id,
            load_balancing_scheme=load_balancing_scheme,
            project=project,
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
        '''Generates CDKTF code for importing a ComputeBackendBucket resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeBackendBucket to import.
        :param import_from_id: The id of the existing ComputeBackendBucket that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeBackendBucket to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a18086429c06047597cdd9f920f1610e86240fd745f00bb638977becf798d0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCdnPolicy")
    def put_cdn_policy(
        self,
        *,
        bypass_cache_on_request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cache_key_policy: typing.Optional[typing.Union["ComputeBackendBucketCdnPolicyCacheKeyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_mode: typing.Optional[builtins.str] = None,
        client_ttl: typing.Optional[jsii.Number] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        max_ttl: typing.Optional[jsii.Number] = None,
        negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negative_caching_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendBucketCdnPolicyNegativeCachingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_coalescing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        serve_while_stale: typing.Optional[jsii.Number] = None,
        signed_url_cache_max_age_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bypass_cache_on_request_headers: bypass_cache_on_request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#bypass_cache_on_request_headers ComputeBackendBucket#bypass_cache_on_request_headers}
        :param cache_key_policy: cache_key_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#cache_key_policy ComputeBackendBucket#cache_key_policy}
        :param cache_mode: Specifies the cache setting for all responses from this backend. The possible values are: USE_ORIGIN_HEADERS, FORCE_CACHE_ALL and CACHE_ALL_STATIC Possible values: ["USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "CACHE_ALL_STATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#cache_mode ComputeBackendBucket#cache_mode}
        :param client_ttl: Specifies the maximum allowed TTL for cached content served by this origin. When the 'cache_mode' is set to "USE_ORIGIN_HEADERS", you must omit this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#client_ttl ComputeBackendBucket#client_ttl}
        :param default_ttl: Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age). When the 'cache_mode' is set to "USE_ORIGIN_HEADERS", you must omit this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#default_ttl ComputeBackendBucket#default_ttl}
        :param max_ttl: Specifies the maximum allowed TTL for cached content served by this origin. When the 'cache_mode' is set to "USE_ORIGIN_HEADERS", you must omit this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#max_ttl ComputeBackendBucket#max_ttl}
        :param negative_caching: Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#negative_caching ComputeBackendBucket#negative_caching}
        :param negative_caching_policy: negative_caching_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#negative_caching_policy ComputeBackendBucket#negative_caching_policy}
        :param request_coalescing: If true then Cloud CDN will combine multiple concurrent cache fill requests into a small number of requests to the origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#request_coalescing ComputeBackendBucket#request_coalescing}
        :param serve_while_stale: Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#serve_while_stale ComputeBackendBucket#serve_while_stale}
        :param signed_url_cache_max_age_sec: Maximum number of seconds the response to a signed URL request will be considered fresh. After this time period, the response will be revalidated before being served. When serving responses to signed URL requests, Cloud CDN will internally behave as though all responses from this backend had a "Cache-Control: public, max-age=[TTL]" header, regardless of any existing Cache-Control header. The actual headers served in responses will not be altered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#signed_url_cache_max_age_sec ComputeBackendBucket#signed_url_cache_max_age_sec}
        '''
        value = ComputeBackendBucketCdnPolicy(
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

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#create ComputeBackendBucket#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#delete ComputeBackendBucket#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#update ComputeBackendBucket#update}.
        '''
        value = ComputeBackendBucketTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCdnPolicy")
    def reset_cdn_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCdnPolicy", []))

    @jsii.member(jsii_name="resetCompressionMode")
    def reset_compression_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompressionMode", []))

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

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoadBalancingScheme")
    def reset_load_balancing_scheme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancingScheme", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="cdnPolicy")
    def cdn_policy(self) -> "ComputeBackendBucketCdnPolicyOutputReference":
        return typing.cast("ComputeBackendBucketCdnPolicyOutputReference", jsii.get(self, "cdnPolicy"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeBackendBucketTimeoutsOutputReference":
        return typing.cast("ComputeBackendBucketTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnPolicyInput")
    def cdn_policy_input(self) -> typing.Optional["ComputeBackendBucketCdnPolicy"]:
        return typing.cast(typing.Optional["ComputeBackendBucketCdnPolicy"], jsii.get(self, "cdnPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionModeInput")
    def compression_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionModeInput"))

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
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingSchemeInput")
    def load_balancing_scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancingSchemeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeBackendBucketTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeBackendBucketTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e74fc96a67c8b7d8d23df5d32f8e0c2feb02f7c41a54c17e606e76a7a3bf290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="compressionMode")
    def compression_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionMode"))

    @compression_mode.setter
    def compression_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08017b912b09f0585aa2a47fb0c243e380652ddd20e3979e7627ce21e3655a30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customResponseHeaders")
    def custom_response_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customResponseHeaders"))

    @custom_response_headers.setter
    def custom_response_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a8ce5dcb3c1faca0c7a63aacbd235a089b2f4ce25d66dcf8827cbb68b1cc469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customResponseHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48eb39df7282441f6b36f43a2c0eb9bded8b58a3a9542320358c65421146fcd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgeSecurityPolicy")
    def edge_security_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeSecurityPolicy"))

    @edge_security_policy.setter
    def edge_security_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3719c58712244b40269ddeb28131c2f0808ae7f876b9df8b467db2bbbff015e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86b29a277dc5a08fe8a27160eb0d7deb753f34aa2a7d4e324bd3ec2e075b76f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableCdn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e268887d2d9981f619b0129a9d3b5a08991ebab88fdcaa17814524e7623327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingScheme")
    def load_balancing_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingScheme"))

    @load_balancing_scheme.setter
    def load_balancing_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c05ef0de938c215a577b1c47a4d06aaab275406ed89c4edc4305163c0e3fafe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingScheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__071eb4a5800eb3817411a7c4c0c15ac5627a241f4ddc3065438baec2136f3401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7083e0ac8b4cbc172b2762c0fb17f89eb053a4f7c79f8c17e63280eec851a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendBucket.ComputeBackendBucketCdnPolicy",
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
class ComputeBackendBucketCdnPolicy:
    def __init__(
        self,
        *,
        bypass_cache_on_request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cache_key_policy: typing.Optional[typing.Union["ComputeBackendBucketCdnPolicyCacheKeyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_mode: typing.Optional[builtins.str] = None,
        client_ttl: typing.Optional[jsii.Number] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        max_ttl: typing.Optional[jsii.Number] = None,
        negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negative_caching_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeBackendBucketCdnPolicyNegativeCachingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_coalescing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        serve_while_stale: typing.Optional[jsii.Number] = None,
        signed_url_cache_max_age_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bypass_cache_on_request_headers: bypass_cache_on_request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#bypass_cache_on_request_headers ComputeBackendBucket#bypass_cache_on_request_headers}
        :param cache_key_policy: cache_key_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#cache_key_policy ComputeBackendBucket#cache_key_policy}
        :param cache_mode: Specifies the cache setting for all responses from this backend. The possible values are: USE_ORIGIN_HEADERS, FORCE_CACHE_ALL and CACHE_ALL_STATIC Possible values: ["USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "CACHE_ALL_STATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#cache_mode ComputeBackendBucket#cache_mode}
        :param client_ttl: Specifies the maximum allowed TTL for cached content served by this origin. When the 'cache_mode' is set to "USE_ORIGIN_HEADERS", you must omit this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#client_ttl ComputeBackendBucket#client_ttl}
        :param default_ttl: Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age). When the 'cache_mode' is set to "USE_ORIGIN_HEADERS", you must omit this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#default_ttl ComputeBackendBucket#default_ttl}
        :param max_ttl: Specifies the maximum allowed TTL for cached content served by this origin. When the 'cache_mode' is set to "USE_ORIGIN_HEADERS", you must omit this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#max_ttl ComputeBackendBucket#max_ttl}
        :param negative_caching: Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#negative_caching ComputeBackendBucket#negative_caching}
        :param negative_caching_policy: negative_caching_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#negative_caching_policy ComputeBackendBucket#negative_caching_policy}
        :param request_coalescing: If true then Cloud CDN will combine multiple concurrent cache fill requests into a small number of requests to the origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#request_coalescing ComputeBackendBucket#request_coalescing}
        :param serve_while_stale: Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#serve_while_stale ComputeBackendBucket#serve_while_stale}
        :param signed_url_cache_max_age_sec: Maximum number of seconds the response to a signed URL request will be considered fresh. After this time period, the response will be revalidated before being served. When serving responses to signed URL requests, Cloud CDN will internally behave as though all responses from this backend had a "Cache-Control: public, max-age=[TTL]" header, regardless of any existing Cache-Control header. The actual headers served in responses will not be altered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#signed_url_cache_max_age_sec ComputeBackendBucket#signed_url_cache_max_age_sec}
        '''
        if isinstance(cache_key_policy, dict):
            cache_key_policy = ComputeBackendBucketCdnPolicyCacheKeyPolicy(**cache_key_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7932b0cef6b829130ae7d65fd0a80ac02b65a8bfec60abadc7a1af12d733017d)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders"]]]:
        '''bypass_cache_on_request_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#bypass_cache_on_request_headers ComputeBackendBucket#bypass_cache_on_request_headers}
        '''
        result = self._values.get("bypass_cache_on_request_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders"]]], result)

    @builtins.property
    def cache_key_policy(
        self,
    ) -> typing.Optional["ComputeBackendBucketCdnPolicyCacheKeyPolicy"]:
        '''cache_key_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#cache_key_policy ComputeBackendBucket#cache_key_policy}
        '''
        result = self._values.get("cache_key_policy")
        return typing.cast(typing.Optional["ComputeBackendBucketCdnPolicyCacheKeyPolicy"], result)

    @builtins.property
    def cache_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the cache setting for all responses from this backend.

        The possible values are: USE_ORIGIN_HEADERS, FORCE_CACHE_ALL and CACHE_ALL_STATIC Possible values: ["USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "CACHE_ALL_STATIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#cache_mode ComputeBackendBucket#cache_mode}
        '''
        result = self._values.get("cache_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_ttl(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum allowed TTL for cached content served by this origin.

        When the
        'cache_mode' is set to "USE_ORIGIN_HEADERS", you must omit this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#client_ttl ComputeBackendBucket#client_ttl}
        '''
        result = self._values.get("client_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_ttl(self) -> typing.Optional[jsii.Number]:
        '''Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age).

        When the 'cache_mode'
        is set to "USE_ORIGIN_HEADERS", you must omit this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#default_ttl ComputeBackendBucket#default_ttl}
        '''
        result = self._values.get("default_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_ttl(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum allowed TTL for cached content served by this origin.

        When the
        'cache_mode' is set to "USE_ORIGIN_HEADERS", you must omit this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#max_ttl ComputeBackendBucket#max_ttl}
        '''
        result = self._values.get("max_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def negative_caching(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#negative_caching ComputeBackendBucket#negative_caching}
        '''
        result = self._values.get("negative_caching")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def negative_caching_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendBucketCdnPolicyNegativeCachingPolicy"]]]:
        '''negative_caching_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#negative_caching_policy ComputeBackendBucket#negative_caching_policy}
        '''
        result = self._values.get("negative_caching_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeBackendBucketCdnPolicyNegativeCachingPolicy"]]], result)

    @builtins.property
    def request_coalescing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true then Cloud CDN will combine multiple concurrent cache fill requests into a small number of requests to the origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#request_coalescing ComputeBackendBucket#request_coalescing}
        '''
        result = self._values.get("request_coalescing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def serve_while_stale(self) -> typing.Optional[jsii.Number]:
        '''Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#serve_while_stale ComputeBackendBucket#serve_while_stale}
        '''
        result = self._values.get("serve_while_stale")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def signed_url_cache_max_age_sec(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of seconds the response to a signed URL request will be considered fresh.

        After this time period,
        the response will be revalidated before being served.
        When serving responses to signed URL requests,
        Cloud CDN will internally behave as though
        all responses from this backend had a "Cache-Control: public,
        max-age=[TTL]" header, regardless of any existing Cache-Control
        header. The actual headers served in responses will not be altered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#signed_url_cache_max_age_sec ComputeBackendBucket#signed_url_cache_max_age_sec}
        '''
        result = self._values.get("signed_url_cache_max_age_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendBucketCdnPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendBucket.ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName"},
)
class ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders:
    def __init__(self, *, header_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param header_name: The header field name to match on when bypassing cache. Values are case-insensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#header_name ComputeBackendBucket#header_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a72e4cc266ece9ca5202185534c68b67b84b58984783ceacd0e14404744f312e)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_name is not None:
            self._values["header_name"] = header_name

    @builtins.property
    def header_name(self) -> typing.Optional[builtins.str]:
        '''The header field name to match on when bypassing cache. Values are case-insensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#header_name ComputeBackendBucket#header_name}
        '''
        result = self._values.get("header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendBucket.ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f89fffa5c7158529a72b4350f8b65d39693eef53a4a8a08951eac5f6fb23c10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a8a571001780bb90e8327716a11ac81408e3289e8ed64b59ba7963a580ba162)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4f879f55889093f6f1c839864ca61a9e496c46125f550cd377ab2140114f84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1f415726c183dffa9ffd547aa0b619d3be829848004812a472619f3d17e4751)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4b605aea2e714a39e47c140b4ffdbb7071011c0dffddbe4fc56a08d014a4f5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b6009d05fe9eef1bbe481ad7c7ce7a1ca1e055544feb7706b7db1e71806a826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendBucket.ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07c79e7b0b0b64146a1101c1a55a3cb5cd24fc66d4ccd1e568b90f7e6e54623d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHeaderName")
    def reset_header_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderName", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__61372c6dc9e02c2a99916241f57242c2abde16ff357748cb96a198224af9a1d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__222f091a25a77a0ec81a507b778f25ac11b58e60aab145eb7f5fabaf380287e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendBucket.ComputeBackendBucketCdnPolicyCacheKeyPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "include_http_headers": "includeHttpHeaders",
        "query_string_whitelist": "queryStringWhitelist",
    },
)
class ComputeBackendBucketCdnPolicyCacheKeyPolicy:
    def __init__(
        self,
        *,
        include_http_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param include_http_headers: Allows HTTP request headers (by name) to be used in the cache key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#include_http_headers ComputeBackendBucket#include_http_headers}
        :param query_string_whitelist: Names of query string parameters to include in cache keys. Default parameters are always included. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#query_string_whitelist ComputeBackendBucket#query_string_whitelist}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8ba77b3005b68d440799aa13dba32c1a7e4f079ff4cdb82fe0c7ee383b4f1d)
            check_type(argname="argument include_http_headers", value=include_http_headers, expected_type=type_hints["include_http_headers"])
            check_type(argname="argument query_string_whitelist", value=query_string_whitelist, expected_type=type_hints["query_string_whitelist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if include_http_headers is not None:
            self._values["include_http_headers"] = include_http_headers
        if query_string_whitelist is not None:
            self._values["query_string_whitelist"] = query_string_whitelist

    @builtins.property
    def include_http_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Allows HTTP request headers (by name) to be used in the cache key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#include_http_headers ComputeBackendBucket#include_http_headers}
        '''
        result = self._values.get("include_http_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_string_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of query string parameters to include in cache keys.

        Default parameters are always included. '&' and '=' will
        be percent encoded and not treated as delimiters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#query_string_whitelist ComputeBackendBucket#query_string_whitelist}
        '''
        result = self._values.get("query_string_whitelist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendBucketCdnPolicyCacheKeyPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendBucketCdnPolicyCacheKeyPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendBucket.ComputeBackendBucketCdnPolicyCacheKeyPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91c02aeb32123274e32cbf528b48cfd00e9820a155fe09e8cf854d84782da200)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeHttpHeaders")
    def reset_include_http_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeHttpHeaders", []))

    @jsii.member(jsii_name="resetQueryStringWhitelist")
    def reset_query_string_whitelist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringWhitelist", []))

    @builtins.property
    @jsii.member(jsii_name="includeHttpHeadersInput")
    def include_http_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeHttpHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringWhitelistInput")
    def query_string_whitelist_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryStringWhitelistInput"))

    @builtins.property
    @jsii.member(jsii_name="includeHttpHeaders")
    def include_http_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeHttpHeaders"))

    @include_http_headers.setter
    def include_http_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a3d831cec3724126056353561400ec8801b707e23e1cc80dc48ef0e24775bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeHttpHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringWhitelist")
    def query_string_whitelist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryStringWhitelist"))

    @query_string_whitelist.setter
    def query_string_whitelist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749a5f8d6db97353628d9f983f318b301cc0cd00442f31305ea5dd085c3d6f93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringWhitelist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeBackendBucketCdnPolicyCacheKeyPolicy]:
        return typing.cast(typing.Optional[ComputeBackendBucketCdnPolicyCacheKeyPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendBucketCdnPolicyCacheKeyPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed5d05de9f45752e1a401034f730ddb08fe64f742fa0662ecf2e178161b8f5cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendBucket.ComputeBackendBucketCdnPolicyNegativeCachingPolicy",
    jsii_struct_bases=[],
    name_mapping={"code": "code", "ttl": "ttl"},
)
class ComputeBackendBucketCdnPolicyNegativeCachingPolicy:
    def __init__(
        self,
        *,
        code: typing.Optional[jsii.Number] = None,
        ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param code: The HTTP status code to define a TTL against. Only HTTP status codes 300, 301, 308, 404, 405, 410, 421, 451 and 501 can be specified as values, and you cannot specify a status code more than once. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#code ComputeBackendBucket#code}
        :param ttl: The TTL (in seconds) for which to cache responses with the corresponding status code. The maximum allowed value is 1800s (30 minutes), noting that infrequently accessed objects may be evicted from the cache before the defined TTL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#ttl ComputeBackendBucket#ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c105cc7fa3d09d144ee018318e9f1197a7cab2940debe2ca37575a542394b9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#code ComputeBackendBucket#code}
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''The TTL (in seconds) for which to cache responses with the corresponding status code.

        The maximum allowed value is 1800s
        (30 minutes), noting that infrequently accessed objects may be evicted from the cache before the defined TTL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#ttl ComputeBackendBucket#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendBucketCdnPolicyNegativeCachingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendBucketCdnPolicyNegativeCachingPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendBucket.ComputeBackendBucketCdnPolicyNegativeCachingPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f6b76564c7d52fcdde4f80209a7bdb6a4e44f3f3789d313e40ccddb16443237)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeBackendBucketCdnPolicyNegativeCachingPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce8221fae5d301896066309d876fa0d18e1611fb5637cb1afdf8f0834aa7378)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeBackendBucketCdnPolicyNegativeCachingPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eacd90fb33e1731f76e4a824c95518d4051a120666efba50424aab8bee24ca4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a91c4b94ba2bab52b683a69d7865f39c6fd97b7e1b3208e73812b7785f1a3d52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43a3fd83162a6d483d63e5ac5707cb08fe9ae389755ed6d5518fe7778e630cca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendBucketCdnPolicyNegativeCachingPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendBucketCdnPolicyNegativeCachingPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendBucketCdnPolicyNegativeCachingPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7813a3d1e2da561cd52777a9c73f8a760c0df32881fbeecb0d39c5ed68109824)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendBucketCdnPolicyNegativeCachingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendBucket.ComputeBackendBucketCdnPolicyNegativeCachingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d448248a8d6cc10bb9ac4f20c9cbd4c83dd5095f6c1ae085cf5226ca164b7244)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f700b71e7b1578d46177457e639acd05425bc044223cc21b20e2c81dd6352c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c728ee22031443f7e4ca77d73d80f21e9593aa4a63f3bafb8e7380aef157e242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendBucketCdnPolicyNegativeCachingPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendBucketCdnPolicyNegativeCachingPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendBucketCdnPolicyNegativeCachingPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff0885f8b34a95c5e5af9b6d12b92785ac11d96cb564f818e5f87d5cc790ea5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeBackendBucketCdnPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendBucket.ComputeBackendBucketCdnPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f75f70bad36d1f19aa689e3c595fd0e2027c90b53d78a17975ca9c2eec9ad0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBypassCacheOnRequestHeaders")
    def put_bypass_cache_on_request_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e70e97eb0ffbfb7842fcc905ae37fde2ce68e1ba2e4ce4a318982cc81cca0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBypassCacheOnRequestHeaders", [value]))

    @jsii.member(jsii_name="putCacheKeyPolicy")
    def put_cache_key_policy(
        self,
        *,
        include_http_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param include_http_headers: Allows HTTP request headers (by name) to be used in the cache key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#include_http_headers ComputeBackendBucket#include_http_headers}
        :param query_string_whitelist: Names of query string parameters to include in cache keys. Default parameters are always included. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#query_string_whitelist ComputeBackendBucket#query_string_whitelist}
        '''
        value = ComputeBackendBucketCdnPolicyCacheKeyPolicy(
            include_http_headers=include_http_headers,
            query_string_whitelist=query_string_whitelist,
        )

        return typing.cast(None, jsii.invoke(self, "putCacheKeyPolicy", [value]))

    @jsii.member(jsii_name="putNegativeCachingPolicy")
    def put_negative_caching_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendBucketCdnPolicyNegativeCachingPolicy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8638df59ca3e232cdf6bd5adc1f139130e16309a79636e1039a4c8c5b477cd4a)
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
    ) -> ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeadersList:
        return typing.cast(ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeadersList, jsii.get(self, "bypassCacheOnRequestHeaders"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyPolicy")
    def cache_key_policy(
        self,
    ) -> ComputeBackendBucketCdnPolicyCacheKeyPolicyOutputReference:
        return typing.cast(ComputeBackendBucketCdnPolicyCacheKeyPolicyOutputReference, jsii.get(self, "cacheKeyPolicy"))

    @builtins.property
    @jsii.member(jsii_name="negativeCachingPolicy")
    def negative_caching_policy(
        self,
    ) -> ComputeBackendBucketCdnPolicyNegativeCachingPolicyList:
        return typing.cast(ComputeBackendBucketCdnPolicyNegativeCachingPolicyList, jsii.get(self, "negativeCachingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="bypassCacheOnRequestHeadersInput")
    def bypass_cache_on_request_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders]]], jsii.get(self, "bypassCacheOnRequestHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyPolicyInput")
    def cache_key_policy_input(
        self,
    ) -> typing.Optional[ComputeBackendBucketCdnPolicyCacheKeyPolicy]:
        return typing.cast(typing.Optional[ComputeBackendBucketCdnPolicyCacheKeyPolicy], jsii.get(self, "cacheKeyPolicyInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendBucketCdnPolicyNegativeCachingPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendBucketCdnPolicyNegativeCachingPolicy]]], jsii.get(self, "negativeCachingPolicyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__aace613c239928c927e79de24488e8c699ead84012c6fb24830245e25b0a87bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTtl")
    def client_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientTtl"))

    @client_ttl.setter
    def client_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944e272d740e8ec4ce46d13b6ef2e01625a9487f645ecee5cc2efe9b8aa27b03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5397dbd773de3cab4d2ef022d0c66e5ba09f079e1771c3fcc886dfe7a7163aac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTtl")
    def max_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxTtl"))

    @max_ttl.setter
    def max_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd2ccf186e4300b7eb5f5396d910ac63a8060c0eec9128a25d4fcc59be52195)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b41c4a44d7427e70afddc0f064cf28658f991dd7be185cb1bdb8cfcca20527fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91a3eedc379eaf97a72d1844ab9fa0bab2a91f380d8d0e5f41c800a6f9aa54d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestCoalescing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serveWhileStale")
    def serve_while_stale(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "serveWhileStale"))

    @serve_while_stale.setter
    def serve_while_stale(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c63f2c92e505c85133d0d78f76e0e13f6ec6e7e19c47f3daa0e96832a0156709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serveWhileStale", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signedUrlCacheMaxAgeSec")
    def signed_url_cache_max_age_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "signedUrlCacheMaxAgeSec"))

    @signed_url_cache_max_age_sec.setter
    def signed_url_cache_max_age_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f774ecc29ffd1f0d9faa63ca9db42f4e01b8f2e7c5cdc627cae384dfb08e3953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signedUrlCacheMaxAgeSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeBackendBucketCdnPolicy]:
        return typing.cast(typing.Optional[ComputeBackendBucketCdnPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeBackendBucketCdnPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b36f112cc524d00208414917ab562053e4774645cae3ac3fa68bb57fd33acfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendBucket.ComputeBackendBucketConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bucket_name": "bucketName",
        "name": "name",
        "cdn_policy": "cdnPolicy",
        "compression_mode": "compressionMode",
        "custom_response_headers": "customResponseHeaders",
        "description": "description",
        "edge_security_policy": "edgeSecurityPolicy",
        "enable_cdn": "enableCdn",
        "id": "id",
        "load_balancing_scheme": "loadBalancingScheme",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class ComputeBackendBucketConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bucket_name: builtins.str,
        name: builtins.str,
        cdn_policy: typing.Optional[typing.Union[ComputeBackendBucketCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        compression_mode: typing.Optional[builtins.str] = None,
        custom_response_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        edge_security_policy: typing.Optional[builtins.str] = None,
        enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeBackendBucketTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bucket_name: Cloud Storage bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#bucket_name ComputeBackendBucket#bucket_name}
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#name ComputeBackendBucket#name}
        :param cdn_policy: cdn_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#cdn_policy ComputeBackendBucket#cdn_policy}
        :param compression_mode: Compress text responses using Brotli or gzip compression, based on the client's Accept-Encoding header. Possible values: ["AUTOMATIC", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#compression_mode ComputeBackendBucket#compression_mode}
        :param custom_response_headers: Headers that the HTTP/S load balancer should add to proxied responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#custom_response_headers ComputeBackendBucket#custom_response_headers}
        :param description: An optional textual description of the resource; provided by the client when the resource is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#description ComputeBackendBucket#description}
        :param edge_security_policy: The security policy associated with this backend bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#edge_security_policy ComputeBackendBucket#edge_security_policy}
        :param enable_cdn: If true, enable Cloud CDN for this BackendBucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#enable_cdn ComputeBackendBucket#enable_cdn}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#id ComputeBackendBucket#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param load_balancing_scheme: The value can only be INTERNAL_MANAGED for cross-region internal layer 7 load balancer. If loadBalancingScheme is not specified, the backend bucket can be used by classic global external load balancers, or global application external load balancers, or both. Possible values: ["INTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#load_balancing_scheme ComputeBackendBucket#load_balancing_scheme}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#project ComputeBackendBucket#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#timeouts ComputeBackendBucket#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cdn_policy, dict):
            cdn_policy = ComputeBackendBucketCdnPolicy(**cdn_policy)
        if isinstance(timeouts, dict):
            timeouts = ComputeBackendBucketTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25d6239e08253d989034f048d3f8c378fafe78f86f997054473404adb98962d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument cdn_policy", value=cdn_policy, expected_type=type_hints["cdn_policy"])
            check_type(argname="argument compression_mode", value=compression_mode, expected_type=type_hints["compression_mode"])
            check_type(argname="argument custom_response_headers", value=custom_response_headers, expected_type=type_hints["custom_response_headers"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument edge_security_policy", value=edge_security_policy, expected_type=type_hints["edge_security_policy"])
            check_type(argname="argument enable_cdn", value=enable_cdn, expected_type=type_hints["enable_cdn"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument load_balancing_scheme", value=load_balancing_scheme, expected_type=type_hints["load_balancing_scheme"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
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
        if cdn_policy is not None:
            self._values["cdn_policy"] = cdn_policy
        if compression_mode is not None:
            self._values["compression_mode"] = compression_mode
        if custom_response_headers is not None:
            self._values["custom_response_headers"] = custom_response_headers
        if description is not None:
            self._values["description"] = description
        if edge_security_policy is not None:
            self._values["edge_security_policy"] = edge_security_policy
        if enable_cdn is not None:
            self._values["enable_cdn"] = enable_cdn
        if id is not None:
            self._values["id"] = id
        if load_balancing_scheme is not None:
            self._values["load_balancing_scheme"] = load_balancing_scheme
        if project is not None:
            self._values["project"] = project
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
    def bucket_name(self) -> builtins.str:
        '''Cloud Storage bucket name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#bucket_name ComputeBackendBucket#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#name ComputeBackendBucket#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cdn_policy(self) -> typing.Optional[ComputeBackendBucketCdnPolicy]:
        '''cdn_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#cdn_policy ComputeBackendBucket#cdn_policy}
        '''
        result = self._values.get("cdn_policy")
        return typing.cast(typing.Optional[ComputeBackendBucketCdnPolicy], result)

    @builtins.property
    def compression_mode(self) -> typing.Optional[builtins.str]:
        '''Compress text responses using Brotli or gzip compression, based on the client's Accept-Encoding header. Possible values: ["AUTOMATIC", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#compression_mode ComputeBackendBucket#compression_mode}
        '''
        result = self._values.get("compression_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_response_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Headers that the HTTP/S load balancer should add to proxied responses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#custom_response_headers ComputeBackendBucket#custom_response_headers}
        '''
        result = self._values.get("custom_response_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional textual description of the resource; provided by the client when the resource is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#description ComputeBackendBucket#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_security_policy(self) -> typing.Optional[builtins.str]:
        '''The security policy associated with this backend bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#edge_security_policy ComputeBackendBucket#edge_security_policy}
        '''
        result = self._values.get("edge_security_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_cdn(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, enable Cloud CDN for this BackendBucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#enable_cdn ComputeBackendBucket#enable_cdn}
        '''
        result = self._values.get("enable_cdn")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#id ComputeBackendBucket#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancing_scheme(self) -> typing.Optional[builtins.str]:
        '''The value can only be INTERNAL_MANAGED for cross-region internal layer 7 load balancer.

        If loadBalancingScheme is not specified, the backend bucket can be used by classic global external load balancers, or global application external load balancers, or both. Possible values: ["INTERNAL_MANAGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#load_balancing_scheme ComputeBackendBucket#load_balancing_scheme}
        '''
        result = self._values.get("load_balancing_scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#project ComputeBackendBucket#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeBackendBucketTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#timeouts ComputeBackendBucket#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeBackendBucketTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendBucketConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeBackendBucket.ComputeBackendBucketTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeBackendBucketTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#create ComputeBackendBucket#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#delete ComputeBackendBucket#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#update ComputeBackendBucket#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25238a67d31aa7bacb2f934c7e5dec4045abe9e23d9ab2d8e1ce464bc7b5de3b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#create ComputeBackendBucket#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#delete ComputeBackendBucket#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_backend_bucket#update ComputeBackendBucket#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeBackendBucketTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeBackendBucketTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeBackendBucket.ComputeBackendBucketTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5cb2ee1457c16e080ce22598eea1011b4c06f4391c58b159addbbb3bc841c2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__178307aae5dd29fe72c1ecf6c776218ed8104e97c726f12cbce621f99ff81629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__485d30e4bda9358141f1b54d4ca481b4e479d5b35b1e5ed8232dd50f49bf5ca6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325c3387d8851a5942bcbc44dad56aac3f7eeb864f5d44045c903c8b31ecb0a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendBucketTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendBucketTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendBucketTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06fcc4ca9bf61b301c4431272f8ed50993da64dce56d36fa7d0390902ed4111e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeBackendBucket",
    "ComputeBackendBucketCdnPolicy",
    "ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders",
    "ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeadersList",
    "ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeadersOutputReference",
    "ComputeBackendBucketCdnPolicyCacheKeyPolicy",
    "ComputeBackendBucketCdnPolicyCacheKeyPolicyOutputReference",
    "ComputeBackendBucketCdnPolicyNegativeCachingPolicy",
    "ComputeBackendBucketCdnPolicyNegativeCachingPolicyList",
    "ComputeBackendBucketCdnPolicyNegativeCachingPolicyOutputReference",
    "ComputeBackendBucketCdnPolicyOutputReference",
    "ComputeBackendBucketConfig",
    "ComputeBackendBucketTimeouts",
    "ComputeBackendBucketTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__db11dd1506b3cd7bdf702512c2e7addc31839c7f7c93549dc6959e22849f3dda(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bucket_name: builtins.str,
    name: builtins.str,
    cdn_policy: typing.Optional[typing.Union[ComputeBackendBucketCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    compression_mode: typing.Optional[builtins.str] = None,
    custom_response_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    edge_security_policy: typing.Optional[builtins.str] = None,
    enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeBackendBucketTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a8a18086429c06047597cdd9f920f1610e86240fd745f00bb638977becf798d0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e74fc96a67c8b7d8d23df5d32f8e0c2feb02f7c41a54c17e606e76a7a3bf290(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08017b912b09f0585aa2a47fb0c243e380652ddd20e3979e7627ce21e3655a30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8ce5dcb3c1faca0c7a63aacbd235a089b2f4ce25d66dcf8827cbb68b1cc469(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48eb39df7282441f6b36f43a2c0eb9bded8b58a3a9542320358c65421146fcd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3719c58712244b40269ddeb28131c2f0808ae7f876b9df8b467db2bbbff015e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b29a277dc5a08fe8a27160eb0d7deb753f34aa2a7d4e324bd3ec2e075b76f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e268887d2d9981f619b0129a9d3b5a08991ebab88fdcaa17814524e7623327(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c05ef0de938c215a577b1c47a4d06aaab275406ed89c4edc4305163c0e3fafe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__071eb4a5800eb3817411a7c4c0c15ac5627a241f4ddc3065438baec2136f3401(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7083e0ac8b4cbc172b2762c0fb17f89eb053a4f7c79f8c17e63280eec851a3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7932b0cef6b829130ae7d65fd0a80ac02b65a8bfec60abadc7a1af12d733017d(
    *,
    bypass_cache_on_request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cache_key_policy: typing.Optional[typing.Union[ComputeBackendBucketCdnPolicyCacheKeyPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    cache_mode: typing.Optional[builtins.str] = None,
    client_ttl: typing.Optional[jsii.Number] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    max_ttl: typing.Optional[jsii.Number] = None,
    negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    negative_caching_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendBucketCdnPolicyNegativeCachingPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_coalescing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    serve_while_stale: typing.Optional[jsii.Number] = None,
    signed_url_cache_max_age_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72e4cc266ece9ca5202185534c68b67b84b58984783ceacd0e14404744f312e(
    *,
    header_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f89fffa5c7158529a72b4350f8b65d39693eef53a4a8a08951eac5f6fb23c10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8a571001780bb90e8327716a11ac81408e3289e8ed64b59ba7963a580ba162(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4f879f55889093f6f1c839864ca61a9e496c46125f550cd377ab2140114f84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f415726c183dffa9ffd547aa0b619d3be829848004812a472619f3d17e4751(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b605aea2e714a39e47c140b4ffdbb7071011c0dffddbe4fc56a08d014a4f5b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6009d05fe9eef1bbe481ad7c7ce7a1ca1e055544feb7706b7db1e71806a826(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c79e7b0b0b64146a1101c1a55a3cb5cd24fc66d4ccd1e568b90f7e6e54623d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61372c6dc9e02c2a99916241f57242c2abde16ff357748cb96a198224af9a1d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222f091a25a77a0ec81a507b778f25ac11b58e60aab145eb7f5fabaf380287e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8ba77b3005b68d440799aa13dba32c1a7e4f079ff4cdb82fe0c7ee383b4f1d(
    *,
    include_http_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c02aeb32123274e32cbf528b48cfd00e9820a155fe09e8cf854d84782da200(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a3d831cec3724126056353561400ec8801b707e23e1cc80dc48ef0e24775bc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749a5f8d6db97353628d9f983f318b301cc0cd00442f31305ea5dd085c3d6f93(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5d05de9f45752e1a401034f730ddb08fe64f742fa0662ecf2e178161b8f5cb(
    value: typing.Optional[ComputeBackendBucketCdnPolicyCacheKeyPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c105cc7fa3d09d144ee018318e9f1197a7cab2940debe2ca37575a542394b9(
    *,
    code: typing.Optional[jsii.Number] = None,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6b76564c7d52fcdde4f80209a7bdb6a4e44f3f3789d313e40ccddb16443237(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce8221fae5d301896066309d876fa0d18e1611fb5637cb1afdf8f0834aa7378(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eacd90fb33e1731f76e4a824c95518d4051a120666efba50424aab8bee24ca4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91c4b94ba2bab52b683a69d7865f39c6fd97b7e1b3208e73812b7785f1a3d52(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a3fd83162a6d483d63e5ac5707cb08fe9ae389755ed6d5518fe7778e630cca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7813a3d1e2da561cd52777a9c73f8a760c0df32881fbeecb0d39c5ed68109824(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeBackendBucketCdnPolicyNegativeCachingPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d448248a8d6cc10bb9ac4f20c9cbd4c83dd5095f6c1ae085cf5226ca164b7244(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f700b71e7b1578d46177457e639acd05425bc044223cc21b20e2c81dd6352c4d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c728ee22031443f7e4ca77d73d80f21e9593aa4a63f3bafb8e7380aef157e242(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0885f8b34a95c5e5af9b6d12b92785ac11d96cb564f818e5f87d5cc790ea5c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendBucketCdnPolicyNegativeCachingPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f75f70bad36d1f19aa689e3c595fd0e2027c90b53d78a17975ca9c2eec9ad0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e70e97eb0ffbfb7842fcc905ae37fde2ce68e1ba2e4ce4a318982cc81cca0f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendBucketCdnPolicyBypassCacheOnRequestHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8638df59ca3e232cdf6bd5adc1f139130e16309a79636e1039a4c8c5b477cd4a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeBackendBucketCdnPolicyNegativeCachingPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aace613c239928c927e79de24488e8c699ead84012c6fb24830245e25b0a87bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944e272d740e8ec4ce46d13b6ef2e01625a9487f645ecee5cc2efe9b8aa27b03(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5397dbd773de3cab4d2ef022d0c66e5ba09f079e1771c3fcc886dfe7a7163aac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd2ccf186e4300b7eb5f5396d910ac63a8060c0eec9128a25d4fcc59be52195(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41c4a44d7427e70afddc0f064cf28658f991dd7be185cb1bdb8cfcca20527fe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a3eedc379eaf97a72d1844ab9fa0bab2a91f380d8d0e5f41c800a6f9aa54d1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c63f2c92e505c85133d0d78f76e0e13f6ec6e7e19c47f3daa0e96832a0156709(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f774ecc29ffd1f0d9faa63ca9db42f4e01b8f2e7c5cdc627cae384dfb08e3953(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b36f112cc524d00208414917ab562053e4774645cae3ac3fa68bb57fd33acfb(
    value: typing.Optional[ComputeBackendBucketCdnPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25d6239e08253d989034f048d3f8c378fafe78f86f997054473404adb98962d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bucket_name: builtins.str,
    name: builtins.str,
    cdn_policy: typing.Optional[typing.Union[ComputeBackendBucketCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    compression_mode: typing.Optional[builtins.str] = None,
    custom_response_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    edge_security_policy: typing.Optional[builtins.str] = None,
    enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeBackendBucketTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25238a67d31aa7bacb2f934c7e5dec4045abe9e23d9ab2d8e1ce464bc7b5de3b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5cb2ee1457c16e080ce22598eea1011b4c06f4391c58b159addbbb3bc841c2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178307aae5dd29fe72c1ecf6c776218ed8104e97c726f12cbce621f99ff81629(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485d30e4bda9358141f1b54d4ca481b4e479d5b35b1e5ed8232dd50f49bf5ca6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325c3387d8851a5942bcbc44dad56aac3f7eeb864f5d44045c903c8b31ecb0a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06fcc4ca9bf61b301c4431272f8ed50993da64dce56d36fa7d0390902ed4111e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeBackendBucketTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
