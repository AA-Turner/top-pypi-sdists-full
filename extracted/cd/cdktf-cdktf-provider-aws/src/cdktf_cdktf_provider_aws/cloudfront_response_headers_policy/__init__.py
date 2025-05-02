r'''
# `aws_cloudfront_response_headers_policy`

Refer to the Terraform Registry for docs: [`aws_cloudfront_response_headers_policy`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy).
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


class CloudfrontResponseHeadersPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy aws_cloudfront_response_headers_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        cors_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyCorsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyCustomHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        etag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        remove_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyRemoveHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        server_timing_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyServerTimingHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy aws_cloudfront_response_headers_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#name CloudfrontResponseHeadersPolicy#name}.
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#comment CloudfrontResponseHeadersPolicy#comment}.
        :param cors_config: cors_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#cors_config CloudfrontResponseHeadersPolicy#cors_config}
        :param custom_headers_config: custom_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#custom_headers_config CloudfrontResponseHeadersPolicy#custom_headers_config}
        :param etag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#etag CloudfrontResponseHeadersPolicy#etag}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#id CloudfrontResponseHeadersPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param remove_headers_config: remove_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#remove_headers_config CloudfrontResponseHeadersPolicy#remove_headers_config}
        :param security_headers_config: security_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#security_headers_config CloudfrontResponseHeadersPolicy#security_headers_config}
        :param server_timing_headers_config: server_timing_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#server_timing_headers_config CloudfrontResponseHeadersPolicy#server_timing_headers_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d209fbf28ef56aed27868de74c25e7c2ecd71c60edd85dc1a295d821b2eae667)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudfrontResponseHeadersPolicyConfig(
            name=name,
            comment=comment,
            cors_config=cors_config,
            custom_headers_config=custom_headers_config,
            etag=etag,
            id=id,
            remove_headers_config=remove_headers_config,
            security_headers_config=security_headers_config,
            server_timing_headers_config=server_timing_headers_config,
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
        '''Generates CDKTF code for importing a CloudfrontResponseHeadersPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudfrontResponseHeadersPolicy to import.
        :param import_from_id: The id of the existing CloudfrontResponseHeadersPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudfrontResponseHeadersPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__504e350ad869e54b2a2461ffb60beef1dc551531151eb7a53966e78cf3db7bbf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCorsConfig")
    def put_cors_config(
        self,
        *,
        access_control_allow_credentials: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        access_control_allow_headers: typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders", typing.Dict[builtins.str, typing.Any]],
        access_control_allow_methods: typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods", typing.Dict[builtins.str, typing.Any]],
        access_control_allow_origins: typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins", typing.Dict[builtins.str, typing.Any]],
        origin_override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        access_control_expose_headers: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders", typing.Dict[builtins.str, typing.Any]]] = None,
        access_control_max_age_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param access_control_allow_credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_credentials CloudfrontResponseHeadersPolicy#access_control_allow_credentials}.
        :param access_control_allow_headers: access_control_allow_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_headers CloudfrontResponseHeadersPolicy#access_control_allow_headers}
        :param access_control_allow_methods: access_control_allow_methods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_methods CloudfrontResponseHeadersPolicy#access_control_allow_methods}
        :param access_control_allow_origins: access_control_allow_origins block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_origins CloudfrontResponseHeadersPolicy#access_control_allow_origins}
        :param origin_override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#origin_override CloudfrontResponseHeadersPolicy#origin_override}.
        :param access_control_expose_headers: access_control_expose_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_expose_headers CloudfrontResponseHeadersPolicy#access_control_expose_headers}
        :param access_control_max_age_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_max_age_sec CloudfrontResponseHeadersPolicy#access_control_max_age_sec}.
        '''
        value = CloudfrontResponseHeadersPolicyCorsConfig(
            access_control_allow_credentials=access_control_allow_credentials,
            access_control_allow_headers=access_control_allow_headers,
            access_control_allow_methods=access_control_allow_methods,
            access_control_allow_origins=access_control_allow_origins,
            origin_override=origin_override,
            access_control_expose_headers=access_control_expose_headers,
            access_control_max_age_sec=access_control_max_age_sec,
        )

        return typing.cast(None, jsii.invoke(self, "putCorsConfig", [value]))

    @jsii.member(jsii_name="putCustomHeadersConfig")
    def put_custom_headers_config(
        self,
        *,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontResponseHeadersPolicyCustomHeadersConfigItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}
        '''
        value = CloudfrontResponseHeadersPolicyCustomHeadersConfig(items=items)

        return typing.cast(None, jsii.invoke(self, "putCustomHeadersConfig", [value]))

    @jsii.member(jsii_name="putRemoveHeadersConfig")
    def put_remove_headers_config(
        self,
        *,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}
        '''
        value = CloudfrontResponseHeadersPolicyRemoveHeadersConfig(items=items)

        return typing.cast(None, jsii.invoke(self, "putRemoveHeadersConfig", [value]))

    @jsii.member(jsii_name="putSecurityHeadersConfig")
    def put_security_headers_config(
        self,
        *,
        content_security_policy: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        content_type_options: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        frame_options: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        referrer_policy: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        strict_transport_security: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity", typing.Dict[builtins.str, typing.Any]]] = None,
        xss_protection: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param content_security_policy: content_security_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#content_security_policy CloudfrontResponseHeadersPolicy#content_security_policy}
        :param content_type_options: content_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#content_type_options CloudfrontResponseHeadersPolicy#content_type_options}
        :param frame_options: frame_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#frame_options CloudfrontResponseHeadersPolicy#frame_options}
        :param referrer_policy: referrer_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#referrer_policy CloudfrontResponseHeadersPolicy#referrer_policy}
        :param strict_transport_security: strict_transport_security block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#strict_transport_security CloudfrontResponseHeadersPolicy#strict_transport_security}
        :param xss_protection: xss_protection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#xss_protection CloudfrontResponseHeadersPolicy#xss_protection}
        '''
        value = CloudfrontResponseHeadersPolicySecurityHeadersConfig(
            content_security_policy=content_security_policy,
            content_type_options=content_type_options,
            frame_options=frame_options,
            referrer_policy=referrer_policy,
            strict_transport_security=strict_transport_security,
            xss_protection=xss_protection,
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityHeadersConfig", [value]))

    @jsii.member(jsii_name="putServerTimingHeadersConfig")
    def put_server_timing_headers_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        sampling_rate: jsii.Number,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#enabled CloudfrontResponseHeadersPolicy#enabled}.
        :param sampling_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#sampling_rate CloudfrontResponseHeadersPolicy#sampling_rate}.
        '''
        value = CloudfrontResponseHeadersPolicyServerTimingHeadersConfig(
            enabled=enabled, sampling_rate=sampling_rate
        )

        return typing.cast(None, jsii.invoke(self, "putServerTimingHeadersConfig", [value]))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetCorsConfig")
    def reset_cors_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCorsConfig", []))

    @jsii.member(jsii_name="resetCustomHeadersConfig")
    def reset_custom_headers_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomHeadersConfig", []))

    @jsii.member(jsii_name="resetEtag")
    def reset_etag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEtag", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRemoveHeadersConfig")
    def reset_remove_headers_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoveHeadersConfig", []))

    @jsii.member(jsii_name="resetSecurityHeadersConfig")
    def reset_security_headers_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityHeadersConfig", []))

    @jsii.member(jsii_name="resetServerTimingHeadersConfig")
    def reset_server_timing_headers_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerTimingHeadersConfig", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="corsConfig")
    def cors_config(self) -> "CloudfrontResponseHeadersPolicyCorsConfigOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicyCorsConfigOutputReference", jsii.get(self, "corsConfig"))

    @builtins.property
    @jsii.member(jsii_name="customHeadersConfig")
    def custom_headers_config(
        self,
    ) -> "CloudfrontResponseHeadersPolicyCustomHeadersConfigOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicyCustomHeadersConfigOutputReference", jsii.get(self, "customHeadersConfig"))

    @builtins.property
    @jsii.member(jsii_name="removeHeadersConfig")
    def remove_headers_config(
        self,
    ) -> "CloudfrontResponseHeadersPolicyRemoveHeadersConfigOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicyRemoveHeadersConfigOutputReference", jsii.get(self, "removeHeadersConfig"))

    @builtins.property
    @jsii.member(jsii_name="securityHeadersConfig")
    def security_headers_config(
        self,
    ) -> "CloudfrontResponseHeadersPolicySecurityHeadersConfigOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicySecurityHeadersConfigOutputReference", jsii.get(self, "securityHeadersConfig"))

    @builtins.property
    @jsii.member(jsii_name="serverTimingHeadersConfig")
    def server_timing_headers_config(
        self,
    ) -> "CloudfrontResponseHeadersPolicyServerTimingHeadersConfigOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicyServerTimingHeadersConfigOutputReference", jsii.get(self, "serverTimingHeadersConfig"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="corsConfigInput")
    def cors_config_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyCorsConfig"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyCorsConfig"], jsii.get(self, "corsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="customHeadersConfigInput")
    def custom_headers_config_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyCustomHeadersConfig"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyCustomHeadersConfig"], jsii.get(self, "customHeadersConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="etagInput")
    def etag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "etagInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="removeHeadersConfigInput")
    def remove_headers_config_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyRemoveHeadersConfig"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyRemoveHeadersConfig"], jsii.get(self, "removeHeadersConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="securityHeadersConfigInput")
    def security_headers_config_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfig"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfig"], jsii.get(self, "securityHeadersConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serverTimingHeadersConfigInput")
    def server_timing_headers_config_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyServerTimingHeadersConfig"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyServerTimingHeadersConfig"], jsii.get(self, "serverTimingHeadersConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7290cc33eafc170ce9e1a81ffc9eb3205b01428d37b00f83e360f8773a4f79f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @etag.setter
    def etag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d205ea3917b8ccc46cb792e120a26255a112ee97db869ad16c60ef9f3ec9af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "etag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0947295438ae03ea85841bc6ed316f26f77292074f5b8ea577cdcc3ccfe9b84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cca81684b174c77fe5af40c47f9dee7eb6eb8bfbb7e58df17f43cdd3fdac650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyConfig",
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
        "comment": "comment",
        "cors_config": "corsConfig",
        "custom_headers_config": "customHeadersConfig",
        "etag": "etag",
        "id": "id",
        "remove_headers_config": "removeHeadersConfig",
        "security_headers_config": "securityHeadersConfig",
        "server_timing_headers_config": "serverTimingHeadersConfig",
    },
)
class CloudfrontResponseHeadersPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        comment: typing.Optional[builtins.str] = None,
        cors_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyCorsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyCustomHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        etag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        remove_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyRemoveHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        server_timing_headers_config: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyServerTimingHeadersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#name CloudfrontResponseHeadersPolicy#name}.
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#comment CloudfrontResponseHeadersPolicy#comment}.
        :param cors_config: cors_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#cors_config CloudfrontResponseHeadersPolicy#cors_config}
        :param custom_headers_config: custom_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#custom_headers_config CloudfrontResponseHeadersPolicy#custom_headers_config}
        :param etag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#etag CloudfrontResponseHeadersPolicy#etag}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#id CloudfrontResponseHeadersPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param remove_headers_config: remove_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#remove_headers_config CloudfrontResponseHeadersPolicy#remove_headers_config}
        :param security_headers_config: security_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#security_headers_config CloudfrontResponseHeadersPolicy#security_headers_config}
        :param server_timing_headers_config: server_timing_headers_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#server_timing_headers_config CloudfrontResponseHeadersPolicy#server_timing_headers_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cors_config, dict):
            cors_config = CloudfrontResponseHeadersPolicyCorsConfig(**cors_config)
        if isinstance(custom_headers_config, dict):
            custom_headers_config = CloudfrontResponseHeadersPolicyCustomHeadersConfig(**custom_headers_config)
        if isinstance(remove_headers_config, dict):
            remove_headers_config = CloudfrontResponseHeadersPolicyRemoveHeadersConfig(**remove_headers_config)
        if isinstance(security_headers_config, dict):
            security_headers_config = CloudfrontResponseHeadersPolicySecurityHeadersConfig(**security_headers_config)
        if isinstance(server_timing_headers_config, dict):
            server_timing_headers_config = CloudfrontResponseHeadersPolicyServerTimingHeadersConfig(**server_timing_headers_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d57043849f08cacd6d164110b30b563e8d0558385130855fa80592185c0be9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument cors_config", value=cors_config, expected_type=type_hints["cors_config"])
            check_type(argname="argument custom_headers_config", value=custom_headers_config, expected_type=type_hints["custom_headers_config"])
            check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument remove_headers_config", value=remove_headers_config, expected_type=type_hints["remove_headers_config"])
            check_type(argname="argument security_headers_config", value=security_headers_config, expected_type=type_hints["security_headers_config"])
            check_type(argname="argument server_timing_headers_config", value=server_timing_headers_config, expected_type=type_hints["server_timing_headers_config"])
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
        if comment is not None:
            self._values["comment"] = comment
        if cors_config is not None:
            self._values["cors_config"] = cors_config
        if custom_headers_config is not None:
            self._values["custom_headers_config"] = custom_headers_config
        if etag is not None:
            self._values["etag"] = etag
        if id is not None:
            self._values["id"] = id
        if remove_headers_config is not None:
            self._values["remove_headers_config"] = remove_headers_config
        if security_headers_config is not None:
            self._values["security_headers_config"] = security_headers_config
        if server_timing_headers_config is not None:
            self._values["server_timing_headers_config"] = server_timing_headers_config

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#name CloudfrontResponseHeadersPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#comment CloudfrontResponseHeadersPolicy#comment}.'''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors_config(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyCorsConfig"]:
        '''cors_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#cors_config CloudfrontResponseHeadersPolicy#cors_config}
        '''
        result = self._values.get("cors_config")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyCorsConfig"], result)

    @builtins.property
    def custom_headers_config(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyCustomHeadersConfig"]:
        '''custom_headers_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#custom_headers_config CloudfrontResponseHeadersPolicy#custom_headers_config}
        '''
        result = self._values.get("custom_headers_config")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyCustomHeadersConfig"], result)

    @builtins.property
    def etag(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#etag CloudfrontResponseHeadersPolicy#etag}.'''
        result = self._values.get("etag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#id CloudfrontResponseHeadersPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remove_headers_config(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyRemoveHeadersConfig"]:
        '''remove_headers_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#remove_headers_config CloudfrontResponseHeadersPolicy#remove_headers_config}
        '''
        result = self._values.get("remove_headers_config")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyRemoveHeadersConfig"], result)

    @builtins.property
    def security_headers_config(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfig"]:
        '''security_headers_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#security_headers_config CloudfrontResponseHeadersPolicy#security_headers_config}
        '''
        result = self._values.get("security_headers_config")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfig"], result)

    @builtins.property
    def server_timing_headers_config(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyServerTimingHeadersConfig"]:
        '''server_timing_headers_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#server_timing_headers_config CloudfrontResponseHeadersPolicy#server_timing_headers_config}
        '''
        result = self._values.get("server_timing_headers_config")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyServerTimingHeadersConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "access_control_allow_credentials": "accessControlAllowCredentials",
        "access_control_allow_headers": "accessControlAllowHeaders",
        "access_control_allow_methods": "accessControlAllowMethods",
        "access_control_allow_origins": "accessControlAllowOrigins",
        "origin_override": "originOverride",
        "access_control_expose_headers": "accessControlExposeHeaders",
        "access_control_max_age_sec": "accessControlMaxAgeSec",
    },
)
class CloudfrontResponseHeadersPolicyCorsConfig:
    def __init__(
        self,
        *,
        access_control_allow_credentials: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        access_control_allow_headers: typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders", typing.Dict[builtins.str, typing.Any]],
        access_control_allow_methods: typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods", typing.Dict[builtins.str, typing.Any]],
        access_control_allow_origins: typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins", typing.Dict[builtins.str, typing.Any]],
        origin_override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        access_control_expose_headers: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders", typing.Dict[builtins.str, typing.Any]]] = None,
        access_control_max_age_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param access_control_allow_credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_credentials CloudfrontResponseHeadersPolicy#access_control_allow_credentials}.
        :param access_control_allow_headers: access_control_allow_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_headers CloudfrontResponseHeadersPolicy#access_control_allow_headers}
        :param access_control_allow_methods: access_control_allow_methods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_methods CloudfrontResponseHeadersPolicy#access_control_allow_methods}
        :param access_control_allow_origins: access_control_allow_origins block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_origins CloudfrontResponseHeadersPolicy#access_control_allow_origins}
        :param origin_override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#origin_override CloudfrontResponseHeadersPolicy#origin_override}.
        :param access_control_expose_headers: access_control_expose_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_expose_headers CloudfrontResponseHeadersPolicy#access_control_expose_headers}
        :param access_control_max_age_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_max_age_sec CloudfrontResponseHeadersPolicy#access_control_max_age_sec}.
        '''
        if isinstance(access_control_allow_headers, dict):
            access_control_allow_headers = CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders(**access_control_allow_headers)
        if isinstance(access_control_allow_methods, dict):
            access_control_allow_methods = CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods(**access_control_allow_methods)
        if isinstance(access_control_allow_origins, dict):
            access_control_allow_origins = CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins(**access_control_allow_origins)
        if isinstance(access_control_expose_headers, dict):
            access_control_expose_headers = CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders(**access_control_expose_headers)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db577ae094cbf1bcd1266fd2ad410ba1cce571835940ca768e72ee6e6db3560)
            check_type(argname="argument access_control_allow_credentials", value=access_control_allow_credentials, expected_type=type_hints["access_control_allow_credentials"])
            check_type(argname="argument access_control_allow_headers", value=access_control_allow_headers, expected_type=type_hints["access_control_allow_headers"])
            check_type(argname="argument access_control_allow_methods", value=access_control_allow_methods, expected_type=type_hints["access_control_allow_methods"])
            check_type(argname="argument access_control_allow_origins", value=access_control_allow_origins, expected_type=type_hints["access_control_allow_origins"])
            check_type(argname="argument origin_override", value=origin_override, expected_type=type_hints["origin_override"])
            check_type(argname="argument access_control_expose_headers", value=access_control_expose_headers, expected_type=type_hints["access_control_expose_headers"])
            check_type(argname="argument access_control_max_age_sec", value=access_control_max_age_sec, expected_type=type_hints["access_control_max_age_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_control_allow_credentials": access_control_allow_credentials,
            "access_control_allow_headers": access_control_allow_headers,
            "access_control_allow_methods": access_control_allow_methods,
            "access_control_allow_origins": access_control_allow_origins,
            "origin_override": origin_override,
        }
        if access_control_expose_headers is not None:
            self._values["access_control_expose_headers"] = access_control_expose_headers
        if access_control_max_age_sec is not None:
            self._values["access_control_max_age_sec"] = access_control_max_age_sec

    @builtins.property
    def access_control_allow_credentials(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_credentials CloudfrontResponseHeadersPolicy#access_control_allow_credentials}.'''
        result = self._values.get("access_control_allow_credentials")
        assert result is not None, "Required property 'access_control_allow_credentials' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def access_control_allow_headers(
        self,
    ) -> "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders":
        '''access_control_allow_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_headers CloudfrontResponseHeadersPolicy#access_control_allow_headers}
        '''
        result = self._values.get("access_control_allow_headers")
        assert result is not None, "Required property 'access_control_allow_headers' is missing"
        return typing.cast("CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders", result)

    @builtins.property
    def access_control_allow_methods(
        self,
    ) -> "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods":
        '''access_control_allow_methods block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_methods CloudfrontResponseHeadersPolicy#access_control_allow_methods}
        '''
        result = self._values.get("access_control_allow_methods")
        assert result is not None, "Required property 'access_control_allow_methods' is missing"
        return typing.cast("CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods", result)

    @builtins.property
    def access_control_allow_origins(
        self,
    ) -> "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins":
        '''access_control_allow_origins block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_allow_origins CloudfrontResponseHeadersPolicy#access_control_allow_origins}
        '''
        result = self._values.get("access_control_allow_origins")
        assert result is not None, "Required property 'access_control_allow_origins' is missing"
        return typing.cast("CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins", result)

    @builtins.property
    def origin_override(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#origin_override CloudfrontResponseHeadersPolicy#origin_override}.'''
        result = self._values.get("origin_override")
        assert result is not None, "Required property 'origin_override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def access_control_expose_headers(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders"]:
        '''access_control_expose_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_expose_headers CloudfrontResponseHeadersPolicy#access_control_expose_headers}
        '''
        result = self._values.get("access_control_expose_headers")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders"], result)

    @builtins.property
    def access_control_max_age_sec(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_max_age_sec CloudfrontResponseHeadersPolicy#access_control_max_age_sec}.'''
        result = self._values.get("access_control_max_age_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyCorsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders",
    jsii_struct_bases=[],
    name_mapping={"items": "items"},
)
class CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders:
    def __init__(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bcc957887cd8dacfb5994ce1024c2408b1e20b3595950e19075e8227703c9ef)
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def items(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.'''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb8644acbcc20ae5164294da2754911f6f1862f88c849b5c6d84d5c87109cb3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "items"))

    @items.setter
    def items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8b4d9127a83fcc8c70ede5a8d2857d5bbd56c62a053650e6d5097323b7ffeb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "items", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3492fb03c9ab48fe229c1e063f4e0b857f44c6ab1afbb00804fd86c4f90d284c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods",
    jsii_struct_bases=[],
    name_mapping={"items": "items"},
)
class CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods:
    def __init__(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aafc127ca5265d75e3fc58e764fe030df27a8e9d06db9c3d585b802a953d494)
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def items(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.'''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethodsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethodsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__367ca38d4ce2b0bba1be8d68a219abb5304f786c4e0a6cd38890f1dcfe340402)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "items"))

    @items.setter
    def items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbf9abc549a62242e9adfec537a595ce79d808a41f98fbc7c1bc18ca1ac95c02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "items", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c9a8ac2fbd15f4ea0e26b3c4d9dd5795228127a795ae2f3a67fa2e7a2fc101e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins",
    jsii_struct_bases=[],
    name_mapping={"items": "items"},
)
class CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins:
    def __init__(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f5f426ed9c15e9c9c1607fe20a0b42af5c69e01a250e7e2a3c370a547b8c3dd)
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def items(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.'''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOriginsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOriginsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__248c20602ab57da36e985f6aade283e67309f05a195f234bbc169847a3d2d021)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "items"))

    @items.setter
    def items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__307cf932305e869fdb17989574447b100536aea87b8627d360c8cd042f944380)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "items", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c23abaeb794fda954177a693f6d0f423fdd7937635eb5a996a3d4bd47a828770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders",
    jsii_struct_bases=[],
    name_mapping={"items": "items"},
)
class CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders:
    def __init__(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864168ef4ebe0d26aebca06da642686c61de41529c7a6501d9787f52e727f464)
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def items(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.'''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c01da90eb72625c5857a623c3138f0de1df85a77b326a42b5543206155830f0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "items"))

    @items.setter
    def items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d274e1a51bcd0db00c8a43b7561fb12896378b63ef6a90c1c91e05026e1238d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "items", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64000227f5769777f1c021b6646129fb64072c1b5e18b624c48831f042786bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontResponseHeadersPolicyCorsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCorsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d26e578d0af0d3975650c3bfdd111ce68d4314a78f8c6cef18f3875b530873c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessControlAllowHeaders")
    def put_access_control_allow_headers(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        value = CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders(
            items=items
        )

        return typing.cast(None, jsii.invoke(self, "putAccessControlAllowHeaders", [value]))

    @jsii.member(jsii_name="putAccessControlAllowMethods")
    def put_access_control_allow_methods(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        value = CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods(
            items=items
        )

        return typing.cast(None, jsii.invoke(self, "putAccessControlAllowMethods", [value]))

    @jsii.member(jsii_name="putAccessControlAllowOrigins")
    def put_access_control_allow_origins(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        value = CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins(
            items=items
        )

        return typing.cast(None, jsii.invoke(self, "putAccessControlAllowOrigins", [value]))

    @jsii.member(jsii_name="putAccessControlExposeHeaders")
    def put_access_control_expose_headers(
        self,
        *,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}.
        '''
        value = CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders(
            items=items
        )

        return typing.cast(None, jsii.invoke(self, "putAccessControlExposeHeaders", [value]))

    @jsii.member(jsii_name="resetAccessControlExposeHeaders")
    def reset_access_control_expose_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessControlExposeHeaders", []))

    @jsii.member(jsii_name="resetAccessControlMaxAgeSec")
    def reset_access_control_max_age_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessControlMaxAgeSec", []))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowHeaders")
    def access_control_allow_headers(
        self,
    ) -> CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeadersOutputReference:
        return typing.cast(CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeadersOutputReference, jsii.get(self, "accessControlAllowHeaders"))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowMethods")
    def access_control_allow_methods(
        self,
    ) -> CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethodsOutputReference:
        return typing.cast(CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethodsOutputReference, jsii.get(self, "accessControlAllowMethods"))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowOrigins")
    def access_control_allow_origins(
        self,
    ) -> CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOriginsOutputReference:
        return typing.cast(CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOriginsOutputReference, jsii.get(self, "accessControlAllowOrigins"))

    @builtins.property
    @jsii.member(jsii_name="accessControlExposeHeaders")
    def access_control_expose_headers(
        self,
    ) -> CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeadersOutputReference:
        return typing.cast(CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeadersOutputReference, jsii.get(self, "accessControlExposeHeaders"))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowCredentialsInput")
    def access_control_allow_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accessControlAllowCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowHeadersInput")
    def access_control_allow_headers_input(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders], jsii.get(self, "accessControlAllowHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowMethodsInput")
    def access_control_allow_methods_input(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods], jsii.get(self, "accessControlAllowMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowOriginsInput")
    def access_control_allow_origins_input(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins], jsii.get(self, "accessControlAllowOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessControlExposeHeadersInput")
    def access_control_expose_headers_input(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders], jsii.get(self, "accessControlExposeHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="accessControlMaxAgeSecInput")
    def access_control_max_age_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accessControlMaxAgeSecInput"))

    @builtins.property
    @jsii.member(jsii_name="originOverrideInput")
    def origin_override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "originOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="accessControlAllowCredentials")
    def access_control_allow_credentials(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "accessControlAllowCredentials"))

    @access_control_allow_credentials.setter
    def access_control_allow_credentials(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caf43a42bf5ca96cba197eed89d0d0f6941e17b7b4881e796866079376cf80fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessControlAllowCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessControlMaxAgeSec")
    def access_control_max_age_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accessControlMaxAgeSec"))

    @access_control_max_age_sec.setter
    def access_control_max_age_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83fdadbb6fc1e3abb785a6e9a7f999bee9b18f42fa46b6ad546473df9a5e2c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessControlMaxAgeSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originOverride")
    def origin_override(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "originOverride"))

    @origin_override.setter
    def origin_override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f99fe79faf2e435e176c2d449373aeee28b9dbc061ac157dc07eaa4aa3823a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originOverride", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCorsConfig]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCorsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ff61312d7d0341c1ec2b74d73529c1793055d999b12ff316f189ac2ac11228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCustomHeadersConfig",
    jsii_struct_bases=[],
    name_mapping={"items": "items"},
)
class CloudfrontResponseHeadersPolicyCustomHeadersConfig:
    def __init__(
        self,
        *,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontResponseHeadersPolicyCustomHeadersConfigItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f363584a6790c44f01d93221760c8af8f0757ed8204e15a441a9afb3888ea8)
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def items(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontResponseHeadersPolicyCustomHeadersConfigItems"]]]:
        '''items block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}
        '''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontResponseHeadersPolicyCustomHeadersConfigItems"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyCustomHeadersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCustomHeadersConfigItems",
    jsii_struct_bases=[],
    name_mapping={"header": "header", "override": "override", "value": "value"},
)
class CloudfrontResponseHeadersPolicyCustomHeadersConfigItems:
    def __init__(
        self,
        *,
        header: builtins.str,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        value: builtins.str,
    ) -> None:
        '''
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#header CloudfrontResponseHeadersPolicy#header}.
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#value CloudfrontResponseHeadersPolicy#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b66a5378dc25d0de9a729c6f0dce06f8e05ad135e5293e6b759da0e446a541)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument override", value=override, expected_type=type_hints["override"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header": header,
            "override": override,
            "value": value,
        }

    @builtins.property
    def header(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#header CloudfrontResponseHeadersPolicy#header}.'''
        result = self._values.get("header")
        assert result is not None, "Required property 'header' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.'''
        result = self._values.get("override")
        assert result is not None, "Required property 'override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#value CloudfrontResponseHeadersPolicy#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyCustomHeadersConfigItems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bae2d413828f0be32a74eafa47bc65f6b84e5465782b5f3583bc81f18adca421)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82c9a48fd846e8b33d30f07712bce97f01aa010107fffc9d078c8030f89e284e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ae71eeea2be363602a938c9f4d65fff72f4196c340cefb1556f2f850eafc71c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3027d79ed1a7052b120fc1472f5aa0ffbe538bf5f69e485515886d16f2de210)
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
            type_hints = typing.get_type_hints(_typecheckingstub__356978b44425369354c7e9b29122f363c081172342851dbaf726a6640af56522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de49f24e8719006529cfb176a62e11170d095b6bc500e060f1742c4b250b6d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f1fe9028924453094a131afd5b9308d1fe0ea74158710d89383475506c87bf5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideInput")
    def override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "header"))

    @header.setter
    def header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c723d82afe4b04c258bbb6eda9878001395a4168095be93a4eef7e5d1729d73c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "header", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="override")
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "override"))

    @override.setter
    def override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__291d5fcd843d7fe5ad91dec270236e3d2da35c5e24be782fe040ed9d78976cd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "override", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc7096dba0ffcfbc946c5bd68e3eaf74234937ffb945e22e4ce644b9aabe7ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca0cbefdcfcaa993dd12a3a9fdc7112b4e43dd027f17f0969f008534365743c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontResponseHeadersPolicyCustomHeadersConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyCustomHeadersConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae7dd0f16191c93b9e083b7c0e267285334010ab433f787ad5dbc0af9fa90b1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putItems")
    def put_items(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47f7b99b46f61042c23f198dc5f651e9b843b69738f027abcfc15617d719204b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putItems", [value]))

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsList:
        return typing.cast(CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsList, jsii.get(self, "items"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyCustomHeadersConfig]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyCustomHeadersConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyCustomHeadersConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6361de597910bc0d9a3299a31cfd86517b20d814c7e66b4e97adb21c458bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyRemoveHeadersConfig",
    jsii_struct_bases=[],
    name_mapping={"items": "items"},
)
class CloudfrontResponseHeadersPolicyRemoveHeadersConfig:
    def __init__(
        self,
        *,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a4418ac7c8dcc9b5da7a5e496dcf06d795378429be610e941ab40eaba872ea)
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def items(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems"]]]:
        '''items block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#items CloudfrontResponseHeadersPolicy#items}
        '''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyRemoveHeadersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems",
    jsii_struct_bases=[],
    name_mapping={"header": "header"},
)
class CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems:
    def __init__(self, *, header: builtins.str) -> None:
        '''
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#header CloudfrontResponseHeadersPolicy#header}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4654d89008c8018683052a4efeba14c30a2c381b2263066f61d7a5d61e75656e)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header": header,
        }

    @builtins.property
    def header(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#header CloudfrontResponseHeadersPolicy#header}.'''
        result = self._values.get("header")
        assert result is not None, "Required property 'header' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc1145be2044884a90458dabda684079f9a47cde2c481414f493a3613dbd4982)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c977c8805cb5bc3d09438064e2944d245004ea5a53408038d49c3dbfaf11696e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ad6c20844c813078ea5016f9ccd552bd9732bcab38fe7402eb29dfcbc1904f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87328cd05ba06fbb2b570678533c8df42091aed087085d101c017fb16be2aaf4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a5c36a6d991f9636f4839d63c17680fe3122d7f686b83d4f919fa76b1a7b512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75a226e2f0aa8eed697f59a075a1a5893c95e6b9cda8dc49b10196f06c141ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b653f55b7ca195ff18920983ed93c472f456a6f910c1f10644c9e3586c57eda0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "header"))

    @header.setter
    def header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d67bc9b941ad48217df5d0f3c48c5918670c61456e0e9e767b9ca3b7990a60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "header", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2500ed08981d8d744a78d7623748744112847a4f8edf0d022fe454849a611c37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontResponseHeadersPolicyRemoveHeadersConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyRemoveHeadersConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__724fe3345fc5057685f2c5e18822fbee0ec25483cc885371814fa187c2b84de0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putItems")
    def put_items(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d766474a7eb9c06f3dbf617cbf2f6c112f25be938da16364d9be5c3c02b9f683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putItems", [value]))

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsList:
        return typing.cast(CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsList, jsii.get(self, "items"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyRemoveHeadersConfig]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyRemoveHeadersConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyRemoveHeadersConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f2a5ab02c42268f8d1b91d539539e8bd3bbf4a59c3cc0afab18692a38e24fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfig",
    jsii_struct_bases=[],
    name_mapping={
        "content_security_policy": "contentSecurityPolicy",
        "content_type_options": "contentTypeOptions",
        "frame_options": "frameOptions",
        "referrer_policy": "referrerPolicy",
        "strict_transport_security": "strictTransportSecurity",
        "xss_protection": "xssProtection",
    },
)
class CloudfrontResponseHeadersPolicySecurityHeadersConfig:
    def __init__(
        self,
        *,
        content_security_policy: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        content_type_options: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        frame_options: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        referrer_policy: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        strict_transport_security: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity", typing.Dict[builtins.str, typing.Any]]] = None,
        xss_protection: typing.Optional[typing.Union["CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param content_security_policy: content_security_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#content_security_policy CloudfrontResponseHeadersPolicy#content_security_policy}
        :param content_type_options: content_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#content_type_options CloudfrontResponseHeadersPolicy#content_type_options}
        :param frame_options: frame_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#frame_options CloudfrontResponseHeadersPolicy#frame_options}
        :param referrer_policy: referrer_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#referrer_policy CloudfrontResponseHeadersPolicy#referrer_policy}
        :param strict_transport_security: strict_transport_security block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#strict_transport_security CloudfrontResponseHeadersPolicy#strict_transport_security}
        :param xss_protection: xss_protection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#xss_protection CloudfrontResponseHeadersPolicy#xss_protection}
        '''
        if isinstance(content_security_policy, dict):
            content_security_policy = CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy(**content_security_policy)
        if isinstance(content_type_options, dict):
            content_type_options = CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions(**content_type_options)
        if isinstance(frame_options, dict):
            frame_options = CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions(**frame_options)
        if isinstance(referrer_policy, dict):
            referrer_policy = CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy(**referrer_policy)
        if isinstance(strict_transport_security, dict):
            strict_transport_security = CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity(**strict_transport_security)
        if isinstance(xss_protection, dict):
            xss_protection = CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection(**xss_protection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77e80601557d50435203f6c39436d99d10b3214d0e01e166e596216c6587321)
            check_type(argname="argument content_security_policy", value=content_security_policy, expected_type=type_hints["content_security_policy"])
            check_type(argname="argument content_type_options", value=content_type_options, expected_type=type_hints["content_type_options"])
            check_type(argname="argument frame_options", value=frame_options, expected_type=type_hints["frame_options"])
            check_type(argname="argument referrer_policy", value=referrer_policy, expected_type=type_hints["referrer_policy"])
            check_type(argname="argument strict_transport_security", value=strict_transport_security, expected_type=type_hints["strict_transport_security"])
            check_type(argname="argument xss_protection", value=xss_protection, expected_type=type_hints["xss_protection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content_security_policy is not None:
            self._values["content_security_policy"] = content_security_policy
        if content_type_options is not None:
            self._values["content_type_options"] = content_type_options
        if frame_options is not None:
            self._values["frame_options"] = frame_options
        if referrer_policy is not None:
            self._values["referrer_policy"] = referrer_policy
        if strict_transport_security is not None:
            self._values["strict_transport_security"] = strict_transport_security
        if xss_protection is not None:
            self._values["xss_protection"] = xss_protection

    @builtins.property
    def content_security_policy(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy"]:
        '''content_security_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#content_security_policy CloudfrontResponseHeadersPolicy#content_security_policy}
        '''
        result = self._values.get("content_security_policy")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy"], result)

    @builtins.property
    def content_type_options(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions"]:
        '''content_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#content_type_options CloudfrontResponseHeadersPolicy#content_type_options}
        '''
        result = self._values.get("content_type_options")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions"], result)

    @builtins.property
    def frame_options(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions"]:
        '''frame_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#frame_options CloudfrontResponseHeadersPolicy#frame_options}
        '''
        result = self._values.get("frame_options")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions"], result)

    @builtins.property
    def referrer_policy(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy"]:
        '''referrer_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#referrer_policy CloudfrontResponseHeadersPolicy#referrer_policy}
        '''
        result = self._values.get("referrer_policy")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy"], result)

    @builtins.property
    def strict_transport_security(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity"]:
        '''strict_transport_security block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#strict_transport_security CloudfrontResponseHeadersPolicy#strict_transport_security}
        '''
        result = self._values.get("strict_transport_security")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity"], result)

    @builtins.property
    def xss_protection(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection"]:
        '''xss_protection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#xss_protection CloudfrontResponseHeadersPolicy#xss_protection}
        '''
        result = self._values.get("xss_protection")
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicySecurityHeadersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "content_security_policy": "contentSecurityPolicy",
        "override": "override",
    },
)
class CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy:
    def __init__(
        self,
        *,
        content_security_policy: builtins.str,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param content_security_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#content_security_policy CloudfrontResponseHeadersPolicy#content_security_policy}.
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967713f2ed8e18c25a664e5b794ce98f99756dcc218836aeb10a75de983afe80)
            check_type(argname="argument content_security_policy", value=content_security_policy, expected_type=type_hints["content_security_policy"])
            check_type(argname="argument override", value=override, expected_type=type_hints["override"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_security_policy": content_security_policy,
            "override": override,
        }

    @builtins.property
    def content_security_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#content_security_policy CloudfrontResponseHeadersPolicy#content_security_policy}.'''
        result = self._values.get("content_security_policy")
        assert result is not None, "Required property 'content_security_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.'''
        result = self._values.get("override")
        assert result is not None, "Required property 'override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46d82b44b304d635d7cf67dca212d6a217142e4cf79dc4856eb5c559644ae31a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="contentSecurityPolicyInput")
    def content_security_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentSecurityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideInput")
    def override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideInput"))

    @builtins.property
    @jsii.member(jsii_name="contentSecurityPolicy")
    def content_security_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentSecurityPolicy"))

    @content_security_policy.setter
    def content_security_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9222fe0884549538feac35c3ba801f199bb075512066e0426f1a215c73f1b232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentSecurityPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="override")
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "override"))

    @override.setter
    def override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4634b6051ac1250110de93a07ba963bb9b45f4affdef789384f2513672c3ecd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "override", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15450ca7238f8312d5f45f6379dca448d649ef7653fe1ebfb1192866d866bccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions",
    jsii_struct_bases=[],
    name_mapping={"override": "override"},
)
class CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions:
    def __init__(
        self,
        *,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bbdba23ac64476aa2d933e5304afe7622ff6a64c96dd0fd9615257f4b474f97)
            check_type(argname="argument override", value=override, expected_type=type_hints["override"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "override": override,
        }

    @builtins.property
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.'''
        result = self._values.get("override")
        assert result is not None, "Required property 'override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fe355e99525e7c5ef166bcfc45e98afa5b1b584d8ffd7df99703207bb844cbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="overrideInput")
    def override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideInput"))

    @builtins.property
    @jsii.member(jsii_name="override")
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "override"))

    @override.setter
    def override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22d0ddba646df337433d23d2e4a5ca721ba6caf4d3ce62a99a764bb38e13c028)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "override", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84b7863798b074aeb578397885d9050514101a368d03ba16abbcee0e86da6832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions",
    jsii_struct_bases=[],
    name_mapping={"frame_option": "frameOption", "override": "override"},
)
class CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions:
    def __init__(
        self,
        *,
        frame_option: builtins.str,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param frame_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#frame_option CloudfrontResponseHeadersPolicy#frame_option}.
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55424da847623d6cd9954ac56532cdc39c9073fd89bc5876824d7999f161ce34)
            check_type(argname="argument frame_option", value=frame_option, expected_type=type_hints["frame_option"])
            check_type(argname="argument override", value=override, expected_type=type_hints["override"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frame_option": frame_option,
            "override": override,
        }

    @builtins.property
    def frame_option(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#frame_option CloudfrontResponseHeadersPolicy#frame_option}.'''
        result = self._values.get("frame_option")
        assert result is not None, "Required property 'frame_option' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.'''
        result = self._values.get("override")
        assert result is not None, "Required property 'override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2247f930171b4babcece539255e36d394c7f924d730bca8a2bde2d9bfaf567c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="frameOptionInput")
    def frame_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frameOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideInput")
    def override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideInput"))

    @builtins.property
    @jsii.member(jsii_name="frameOption")
    def frame_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frameOption"))

    @frame_option.setter
    def frame_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc862645aea0a82b5125c87efdf3b528782874622e1f46186fa991a4af9a5a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frameOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="override")
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "override"))

    @override.setter
    def override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9daa5cd2b24901b682ff1ef34dc7c9e43f4ad6d85ede776c73365f6212a265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "override", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891ae2d798ff832a6a91476e6882e77834e350e791a58e6d7344d2fb6837d478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontResponseHeadersPolicySecurityHeadersConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41853808f38b17f2521129fba0e3744ba7b2dfd822819e654c484398cdaadb6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContentSecurityPolicy")
    def put_content_security_policy(
        self,
        *,
        content_security_policy: builtins.str,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param content_security_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#content_security_policy CloudfrontResponseHeadersPolicy#content_security_policy}.
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        '''
        value = CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy(
            content_security_policy=content_security_policy, override=override
        )

        return typing.cast(None, jsii.invoke(self, "putContentSecurityPolicy", [value]))

    @jsii.member(jsii_name="putContentTypeOptions")
    def put_content_type_options(
        self,
        *,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        '''
        value = CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions(
            override=override
        )

        return typing.cast(None, jsii.invoke(self, "putContentTypeOptions", [value]))

    @jsii.member(jsii_name="putFrameOptions")
    def put_frame_options(
        self,
        *,
        frame_option: builtins.str,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param frame_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#frame_option CloudfrontResponseHeadersPolicy#frame_option}.
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        '''
        value = CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions(
            frame_option=frame_option, override=override
        )

        return typing.cast(None, jsii.invoke(self, "putFrameOptions", [value]))

    @jsii.member(jsii_name="putReferrerPolicy")
    def put_referrer_policy(
        self,
        *,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        referrer_policy: builtins.str,
    ) -> None:
        '''
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        :param referrer_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#referrer_policy CloudfrontResponseHeadersPolicy#referrer_policy}.
        '''
        value = CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy(
            override=override, referrer_policy=referrer_policy
        )

        return typing.cast(None, jsii.invoke(self, "putReferrerPolicy", [value]))

    @jsii.member(jsii_name="putStrictTransportSecurity")
    def put_strict_transport_security(
        self,
        *,
        access_control_max_age_sec: jsii.Number,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        include_subdomains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        preload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_control_max_age_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_max_age_sec CloudfrontResponseHeadersPolicy#access_control_max_age_sec}.
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        :param include_subdomains: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#include_subdomains CloudfrontResponseHeadersPolicy#include_subdomains}.
        :param preload: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#preload CloudfrontResponseHeadersPolicy#preload}.
        '''
        value = CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity(
            access_control_max_age_sec=access_control_max_age_sec,
            override=override,
            include_subdomains=include_subdomains,
            preload=preload,
        )

        return typing.cast(None, jsii.invoke(self, "putStrictTransportSecurity", [value]))

    @jsii.member(jsii_name="putXssProtection")
    def put_xss_protection(
        self,
        *,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        protection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        mode_block: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        report_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        :param protection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#protection CloudfrontResponseHeadersPolicy#protection}.
        :param mode_block: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#mode_block CloudfrontResponseHeadersPolicy#mode_block}.
        :param report_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#report_uri CloudfrontResponseHeadersPolicy#report_uri}.
        '''
        value = CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection(
            override=override,
            protection=protection,
            mode_block=mode_block,
            report_uri=report_uri,
        )

        return typing.cast(None, jsii.invoke(self, "putXssProtection", [value]))

    @jsii.member(jsii_name="resetContentSecurityPolicy")
    def reset_content_security_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentSecurityPolicy", []))

    @jsii.member(jsii_name="resetContentTypeOptions")
    def reset_content_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentTypeOptions", []))

    @jsii.member(jsii_name="resetFrameOptions")
    def reset_frame_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrameOptions", []))

    @jsii.member(jsii_name="resetReferrerPolicy")
    def reset_referrer_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferrerPolicy", []))

    @jsii.member(jsii_name="resetStrictTransportSecurity")
    def reset_strict_transport_security(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrictTransportSecurity", []))

    @jsii.member(jsii_name="resetXssProtection")
    def reset_xss_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXssProtection", []))

    @builtins.property
    @jsii.member(jsii_name="contentSecurityPolicy")
    def content_security_policy(
        self,
    ) -> CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicyOutputReference:
        return typing.cast(CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicyOutputReference, jsii.get(self, "contentSecurityPolicy"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeOptions")
    def content_type_options(
        self,
    ) -> CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptionsOutputReference:
        return typing.cast(CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptionsOutputReference, jsii.get(self, "contentTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="frameOptions")
    def frame_options(
        self,
    ) -> CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptionsOutputReference:
        return typing.cast(CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptionsOutputReference, jsii.get(self, "frameOptions"))

    @builtins.property
    @jsii.member(jsii_name="referrerPolicy")
    def referrer_policy(
        self,
    ) -> "CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicyOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicyOutputReference", jsii.get(self, "referrerPolicy"))

    @builtins.property
    @jsii.member(jsii_name="strictTransportSecurity")
    def strict_transport_security(
        self,
    ) -> "CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurityOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurityOutputReference", jsii.get(self, "strictTransportSecurity"))

    @builtins.property
    @jsii.member(jsii_name="xssProtection")
    def xss_protection(
        self,
    ) -> "CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtectionOutputReference":
        return typing.cast("CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtectionOutputReference", jsii.get(self, "xssProtection"))

    @builtins.property
    @jsii.member(jsii_name="contentSecurityPolicyInput")
    def content_security_policy_input(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy], jsii.get(self, "contentSecurityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeOptionsInput")
    def content_type_options_input(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions], jsii.get(self, "contentTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="frameOptionsInput")
    def frame_options_input(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions], jsii.get(self, "frameOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="referrerPolicyInput")
    def referrer_policy_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy"], jsii.get(self, "referrerPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="strictTransportSecurityInput")
    def strict_transport_security_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity"], jsii.get(self, "strictTransportSecurityInput"))

    @builtins.property
    @jsii.member(jsii_name="xssProtectionInput")
    def xss_protection_input(
        self,
    ) -> typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection"]:
        return typing.cast(typing.Optional["CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection"], jsii.get(self, "xssProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfig]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43320dcb266475f0d7e02ab30a687386d941d60e0f7d8cb90df94e6fe4325dee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy",
    jsii_struct_bases=[],
    name_mapping={"override": "override", "referrer_policy": "referrerPolicy"},
)
class CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy:
    def __init__(
        self,
        *,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        referrer_policy: builtins.str,
    ) -> None:
        '''
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        :param referrer_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#referrer_policy CloudfrontResponseHeadersPolicy#referrer_policy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b89a201d947af795de0d14414b95ac25db86984938f9db4bcf09269e6b05d2c)
            check_type(argname="argument override", value=override, expected_type=type_hints["override"])
            check_type(argname="argument referrer_policy", value=referrer_policy, expected_type=type_hints["referrer_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "override": override,
            "referrer_policy": referrer_policy,
        }

    @builtins.property
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.'''
        result = self._values.get("override")
        assert result is not None, "Required property 'override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def referrer_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#referrer_policy CloudfrontResponseHeadersPolicy#referrer_policy}.'''
        result = self._values.get("referrer_policy")
        assert result is not None, "Required property 'referrer_policy' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b5722acdabf72d8340ead34ae0c3912a712e1a0b0560623b9deb37d9605d903)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="overrideInput")
    def override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideInput"))

    @builtins.property
    @jsii.member(jsii_name="referrerPolicyInput")
    def referrer_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "referrerPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="override")
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "override"))

    @override.setter
    def override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__938c831e883b6e02531a38d57309a5f48fcc3e4c55a7b063f40ee4e0b0c93a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "override", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="referrerPolicy")
    def referrer_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "referrerPolicy"))

    @referrer_policy.setter
    def referrer_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f74f8161609c940a5a315187d274aa81020388aa6c5333e65d00e397b1a2ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referrerPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39bf0fa1318b874d527daf761d71306f76229ce75f88963455dce5e805931565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity",
    jsii_struct_bases=[],
    name_mapping={
        "access_control_max_age_sec": "accessControlMaxAgeSec",
        "override": "override",
        "include_subdomains": "includeSubdomains",
        "preload": "preload",
    },
)
class CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity:
    def __init__(
        self,
        *,
        access_control_max_age_sec: jsii.Number,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        include_subdomains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        preload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_control_max_age_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_max_age_sec CloudfrontResponseHeadersPolicy#access_control_max_age_sec}.
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        :param include_subdomains: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#include_subdomains CloudfrontResponseHeadersPolicy#include_subdomains}.
        :param preload: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#preload CloudfrontResponseHeadersPolicy#preload}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a21181eac9b0a002b0c62197967127a8d2e926f3fda0d6e1d5b4fd63d90262df)
            check_type(argname="argument access_control_max_age_sec", value=access_control_max_age_sec, expected_type=type_hints["access_control_max_age_sec"])
            check_type(argname="argument override", value=override, expected_type=type_hints["override"])
            check_type(argname="argument include_subdomains", value=include_subdomains, expected_type=type_hints["include_subdomains"])
            check_type(argname="argument preload", value=preload, expected_type=type_hints["preload"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_control_max_age_sec": access_control_max_age_sec,
            "override": override,
        }
        if include_subdomains is not None:
            self._values["include_subdomains"] = include_subdomains
        if preload is not None:
            self._values["preload"] = preload

    @builtins.property
    def access_control_max_age_sec(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#access_control_max_age_sec CloudfrontResponseHeadersPolicy#access_control_max_age_sec}.'''
        result = self._values.get("access_control_max_age_sec")
        assert result is not None, "Required property 'access_control_max_age_sec' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.'''
        result = self._values.get("override")
        assert result is not None, "Required property 'override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def include_subdomains(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#include_subdomains CloudfrontResponseHeadersPolicy#include_subdomains}.'''
        result = self._values.get("include_subdomains")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def preload(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#preload CloudfrontResponseHeadersPolicy#preload}.'''
        result = self._values.get("preload")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea9ecc4e1f1c82f18c5450317afd7dd9594fb3a7363afc206b77915af57ab354)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeSubdomains")
    def reset_include_subdomains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeSubdomains", []))

    @jsii.member(jsii_name="resetPreload")
    def reset_preload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreload", []))

    @builtins.property
    @jsii.member(jsii_name="accessControlMaxAgeSecInput")
    def access_control_max_age_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accessControlMaxAgeSecInput"))

    @builtins.property
    @jsii.member(jsii_name="includeSubdomainsInput")
    def include_subdomains_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeSubdomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideInput")
    def override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideInput"))

    @builtins.property
    @jsii.member(jsii_name="preloadInput")
    def preload_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preloadInput"))

    @builtins.property
    @jsii.member(jsii_name="accessControlMaxAgeSec")
    def access_control_max_age_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accessControlMaxAgeSec"))

    @access_control_max_age_sec.setter
    def access_control_max_age_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1214cdc85e14ad808f3806fc59d30015e8b147c53243a0af9146b0fab97827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessControlMaxAgeSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeSubdomains")
    def include_subdomains(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeSubdomains"))

    @include_subdomains.setter
    def include_subdomains(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c889086053f7a7f53601450448184217100f1755c48cb62745cf7f1438c267)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeSubdomains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="override")
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "override"))

    @override.setter
    def override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b28bb4c81503a692777cf72f8d4a1cdfdd46d867c8c76770a689e0b51d92024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "override", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preload")
    def preload(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preload"))

    @preload.setter
    def preload(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5e87e6efb4441ca5554001c9863818a45de156ce666d3f678a830c0c01a55a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a046a019e850138ae3c71b4bd231d2ab8d33c2e9345ee053086cafd4df11967b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection",
    jsii_struct_bases=[],
    name_mapping={
        "override": "override",
        "protection": "protection",
        "mode_block": "modeBlock",
        "report_uri": "reportUri",
    },
)
class CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection:
    def __init__(
        self,
        *,
        override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        protection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        mode_block: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        report_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.
        :param protection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#protection CloudfrontResponseHeadersPolicy#protection}.
        :param mode_block: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#mode_block CloudfrontResponseHeadersPolicy#mode_block}.
        :param report_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#report_uri CloudfrontResponseHeadersPolicy#report_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab5b6c0fad6b0054d59632b0adbd9d356022c36aa9f6ba888f292f4645fc5fc8)
            check_type(argname="argument override", value=override, expected_type=type_hints["override"])
            check_type(argname="argument protection", value=protection, expected_type=type_hints["protection"])
            check_type(argname="argument mode_block", value=mode_block, expected_type=type_hints["mode_block"])
            check_type(argname="argument report_uri", value=report_uri, expected_type=type_hints["report_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "override": override,
            "protection": protection,
        }
        if mode_block is not None:
            self._values["mode_block"] = mode_block
        if report_uri is not None:
            self._values["report_uri"] = report_uri

    @builtins.property
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#override CloudfrontResponseHeadersPolicy#override}.'''
        result = self._values.get("override")
        assert result is not None, "Required property 'override' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def protection(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#protection CloudfrontResponseHeadersPolicy#protection}.'''
        result = self._values.get("protection")
        assert result is not None, "Required property 'protection' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def mode_block(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#mode_block CloudfrontResponseHeadersPolicy#mode_block}.'''
        result = self._values.get("mode_block")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def report_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#report_uri CloudfrontResponseHeadersPolicy#report_uri}.'''
        result = self._values.get("report_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f079c1338c91faf953c971388a691865fa76df29701ee1b84dd6551bb085cb97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetModeBlock")
    def reset_mode_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModeBlock", []))

    @jsii.member(jsii_name="resetReportUri")
    def reset_report_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReportUri", []))

    @builtins.property
    @jsii.member(jsii_name="modeBlockInput")
    def mode_block_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "modeBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideInput")
    def override_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideInput"))

    @builtins.property
    @jsii.member(jsii_name="protectionInput")
    def protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "protectionInput"))

    @builtins.property
    @jsii.member(jsii_name="reportUriInput")
    def report_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reportUriInput"))

    @builtins.property
    @jsii.member(jsii_name="modeBlock")
    def mode_block(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "modeBlock"))

    @mode_block.setter
    def mode_block(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5df3b832457b1fe2d3b9d797014a88bb7afa9f3dc0a138bcc4c2cc60595c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modeBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="override")
    def override(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "override"))

    @override.setter
    def override(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1bd8bffe8fd51e252e65a088ee049bf669fd4d811f4a61109e11c59d0658422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "override", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protection")
    def protection(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "protection"))

    @protection.setter
    def protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1386aa0a14ab45964e97b05e994918964b8df0b143c49cbe9d86e912bd18521c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reportUri")
    def report_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reportUri"))

    @report_uri.setter
    def report_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__049f7ffff746dd989d61c64e4dcf0c8db2e4d5b5740ebd0b0c386d779cb137af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reportUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00a3aa3d74a2ad2132b8c944f6dfabba98f631df84b10d855810159659a717e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyServerTimingHeadersConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "sampling_rate": "samplingRate"},
)
class CloudfrontResponseHeadersPolicyServerTimingHeadersConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        sampling_rate: jsii.Number,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#enabled CloudfrontResponseHeadersPolicy#enabled}.
        :param sampling_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#sampling_rate CloudfrontResponseHeadersPolicy#sampling_rate}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9c6a2d5601796f69cf7b8698976ff23e55e932f1a7dd07ee7c0e83ccc26bf9)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument sampling_rate", value=sampling_rate, expected_type=type_hints["sampling_rate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "sampling_rate": sampling_rate,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#enabled CloudfrontResponseHeadersPolicy#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def sampling_rate(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/cloudfront_response_headers_policy#sampling_rate CloudfrontResponseHeadersPolicy#sampling_rate}.'''
        result = self._values.get("sampling_rate")
        assert result is not None, "Required property 'sampling_rate' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontResponseHeadersPolicyServerTimingHeadersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontResponseHeadersPolicyServerTimingHeadersConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudfrontResponseHeadersPolicy.CloudfrontResponseHeadersPolicyServerTimingHeadersConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dd961a1c09e691a73e5e2d41916ab27ecdbad80236f1a04fadf3ff8bbd8c0b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="samplingRateInput")
    def sampling_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "samplingRateInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cdd2d1a17757c7c7f315bbcf817a0cfdf16dc44beec67b7468326483e39dcc30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samplingRate")
    def sampling_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "samplingRate"))

    @sampling_rate.setter
    def sampling_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0a49b1757392f62a2ab95c85258f69948226ed2189022cd6583162dc4461a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontResponseHeadersPolicyServerTimingHeadersConfig]:
        return typing.cast(typing.Optional[CloudfrontResponseHeadersPolicyServerTimingHeadersConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontResponseHeadersPolicyServerTimingHeadersConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3c03a7d18b2541970001cbb42068f81cbdb457553aa212dd20f58c5f869c6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudfrontResponseHeadersPolicy",
    "CloudfrontResponseHeadersPolicyConfig",
    "CloudfrontResponseHeadersPolicyCorsConfig",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeadersOutputReference",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethodsOutputReference",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOriginsOutputReference",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders",
    "CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeadersOutputReference",
    "CloudfrontResponseHeadersPolicyCorsConfigOutputReference",
    "CloudfrontResponseHeadersPolicyCustomHeadersConfig",
    "CloudfrontResponseHeadersPolicyCustomHeadersConfigItems",
    "CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsList",
    "CloudfrontResponseHeadersPolicyCustomHeadersConfigItemsOutputReference",
    "CloudfrontResponseHeadersPolicyCustomHeadersConfigOutputReference",
    "CloudfrontResponseHeadersPolicyRemoveHeadersConfig",
    "CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems",
    "CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsList",
    "CloudfrontResponseHeadersPolicyRemoveHeadersConfigItemsOutputReference",
    "CloudfrontResponseHeadersPolicyRemoveHeadersConfigOutputReference",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfig",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicyOutputReference",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptionsOutputReference",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptionsOutputReference",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigOutputReference",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicyOutputReference",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurityOutputReference",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection",
    "CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtectionOutputReference",
    "CloudfrontResponseHeadersPolicyServerTimingHeadersConfig",
    "CloudfrontResponseHeadersPolicyServerTimingHeadersConfigOutputReference",
]

publication.publish()

def _typecheckingstub__d209fbf28ef56aed27868de74c25e7c2ecd71c60edd85dc1a295d821b2eae667(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    cors_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyCorsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyCustomHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    etag: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    remove_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyRemoveHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    security_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    server_timing_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyServerTimingHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__504e350ad869e54b2a2461ffb60beef1dc551531151eb7a53966e78cf3db7bbf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7290cc33eafc170ce9e1a81ffc9eb3205b01428d37b00f83e360f8773a4f79f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d205ea3917b8ccc46cb792e120a26255a112ee97db869ad16c60ef9f3ec9af5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0947295438ae03ea85841bc6ed316f26f77292074f5b8ea577cdcc3ccfe9b84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cca81684b174c77fe5af40c47f9dee7eb6eb8bfbb7e58df17f43cdd3fdac650(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d57043849f08cacd6d164110b30b563e8d0558385130855fa80592185c0be9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    cors_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyCorsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyCustomHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    etag: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    remove_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyRemoveHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    security_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    server_timing_headers_config: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyServerTimingHeadersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db577ae094cbf1bcd1266fd2ad410ba1cce571835940ca768e72ee6e6db3560(
    *,
    access_control_allow_credentials: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    access_control_allow_headers: typing.Union[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders, typing.Dict[builtins.str, typing.Any]],
    access_control_allow_methods: typing.Union[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods, typing.Dict[builtins.str, typing.Any]],
    access_control_allow_origins: typing.Union[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins, typing.Dict[builtins.str, typing.Any]],
    origin_override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    access_control_expose_headers: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders, typing.Dict[builtins.str, typing.Any]]] = None,
    access_control_max_age_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bcc957887cd8dacfb5994ce1024c2408b1e20b3595950e19075e8227703c9ef(
    *,
    items: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8644acbcc20ae5164294da2754911f6f1862f88c849b5c6d84d5c87109cb3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b4d9127a83fcc8c70ede5a8d2857d5bbd56c62a053650e6d5097323b7ffeb2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3492fb03c9ab48fe229c1e063f4e0b857f44c6ab1afbb00804fd86c4f90d284c(
    value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowHeaders],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aafc127ca5265d75e3fc58e764fe030df27a8e9d06db9c3d585b802a953d494(
    *,
    items: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367ca38d4ce2b0bba1be8d68a219abb5304f786c4e0a6cd38890f1dcfe340402(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf9abc549a62242e9adfec537a595ce79d808a41f98fbc7c1bc18ca1ac95c02(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c9a8ac2fbd15f4ea0e26b3c4d9dd5795228127a795ae2f3a67fa2e7a2fc101e(
    value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowMethods],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5f426ed9c15e9c9c1607fe20a0b42af5c69e01a250e7e2a3c370a547b8c3dd(
    *,
    items: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248c20602ab57da36e985f6aade283e67309f05a195f234bbc169847a3d2d021(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307cf932305e869fdb17989574447b100536aea87b8627d360c8cd042f944380(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c23abaeb794fda954177a693f6d0f423fdd7937635eb5a996a3d4bd47a828770(
    value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlAllowOrigins],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864168ef4ebe0d26aebca06da642686c61de41529c7a6501d9787f52e727f464(
    *,
    items: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01da90eb72625c5857a623c3138f0de1df85a77b326a42b5543206155830f0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d274e1a51bcd0db00c8a43b7561fb12896378b63ef6a90c1c91e05026e1238d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64000227f5769777f1c021b6646129fb64072c1b5e18b624c48831f042786bf(
    value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfigAccessControlExposeHeaders],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d26e578d0af0d3975650c3bfdd111ce68d4314a78f8c6cef18f3875b530873c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf43a42bf5ca96cba197eed89d0d0f6941e17b7b4881e796866079376cf80fb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83fdadbb6fc1e3abb785a6e9a7f999bee9b18f42fa46b6ad546473df9a5e2c09(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f99fe79faf2e435e176c2d449373aeee28b9dbc061ac157dc07eaa4aa3823a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ff61312d7d0341c1ec2b74d73529c1793055d999b12ff316f189ac2ac11228(
    value: typing.Optional[CloudfrontResponseHeadersPolicyCorsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f363584a6790c44f01d93221760c8af8f0757ed8204e15a441a9afb3888ea8(
    *,
    items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b66a5378dc25d0de9a729c6f0dce06f8e05ad135e5293e6b759da0e446a541(
    *,
    header: builtins.str,
    override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae2d413828f0be32a74eafa47bc65f6b84e5465782b5f3583bc81f18adca421(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c9a48fd846e8b33d30f07712bce97f01aa010107fffc9d078c8030f89e284e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae71eeea2be363602a938c9f4d65fff72f4196c340cefb1556f2f850eafc71c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3027d79ed1a7052b120fc1472f5aa0ffbe538bf5f69e485515886d16f2de210(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356978b44425369354c7e9b29122f363c081172342851dbaf726a6640af56522(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de49f24e8719006529cfb176a62e11170d095b6bc500e060f1742c4b250b6d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1fe9028924453094a131afd5b9308d1fe0ea74158710d89383475506c87bf5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c723d82afe4b04c258bbb6eda9878001395a4168095be93a4eef7e5d1729d73c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291d5fcd843d7fe5ad91dec270236e3d2da35c5e24be782fe040ed9d78976cd5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc7096dba0ffcfbc946c5bd68e3eaf74234937ffb945e22e4ce644b9aabe7ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca0cbefdcfcaa993dd12a3a9fdc7112b4e43dd027f17f0969f008534365743c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyCustomHeadersConfigItems]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae7dd0f16191c93b9e083b7c0e267285334010ab433f787ad5dbc0af9fa90b1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f7b99b46f61042c23f198dc5f651e9b843b69738f027abcfc15617d719204b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontResponseHeadersPolicyCustomHeadersConfigItems, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6361de597910bc0d9a3299a31cfd86517b20d814c7e66b4e97adb21c458bd8(
    value: typing.Optional[CloudfrontResponseHeadersPolicyCustomHeadersConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a4418ac7c8dcc9b5da7a5e496dcf06d795378429be610e941ab40eaba872ea(
    *,
    items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4654d89008c8018683052a4efeba14c30a2c381b2263066f61d7a5d61e75656e(
    *,
    header: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1145be2044884a90458dabda684079f9a47cde2c481414f493a3613dbd4982(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c977c8805cb5bc3d09438064e2944d245004ea5a53408038d49c3dbfaf11696e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ad6c20844c813078ea5016f9ccd552bd9732bcab38fe7402eb29dfcbc1904f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87328cd05ba06fbb2b570678533c8df42091aed087085d101c017fb16be2aaf4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5c36a6d991f9636f4839d63c17680fe3122d7f686b83d4f919fa76b1a7b512(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75a226e2f0aa8eed697f59a075a1a5893c95e6b9cda8dc49b10196f06c141ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b653f55b7ca195ff18920983ed93c472f456a6f910c1f10644c9e3586c57eda0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d67bc9b941ad48217df5d0f3c48c5918670c61456e0e9e767b9ca3b7990a60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2500ed08981d8d744a78d7623748744112847a4f8edf0d022fe454849a611c37(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724fe3345fc5057685f2c5e18822fbee0ec25483cc885371814fa187c2b84de0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d766474a7eb9c06f3dbf617cbf2f6c112f25be938da16364d9be5c3c02b9f683(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontResponseHeadersPolicyRemoveHeadersConfigItems, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f2a5ab02c42268f8d1b91d539539e8bd3bbf4a59c3cc0afab18692a38e24fb(
    value: typing.Optional[CloudfrontResponseHeadersPolicyRemoveHeadersConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77e80601557d50435203f6c39436d99d10b3214d0e01e166e596216c6587321(
    *,
    content_security_policy: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    content_type_options: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    frame_options: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    referrer_policy: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    strict_transport_security: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity, typing.Dict[builtins.str, typing.Any]]] = None,
    xss_protection: typing.Optional[typing.Union[CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967713f2ed8e18c25a664e5b794ce98f99756dcc218836aeb10a75de983afe80(
    *,
    content_security_policy: builtins.str,
    override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d82b44b304d635d7cf67dca212d6a217142e4cf79dc4856eb5c559644ae31a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9222fe0884549538feac35c3ba801f199bb075512066e0426f1a215c73f1b232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4634b6051ac1250110de93a07ba963bb9b45f4affdef789384f2513672c3ecd4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15450ca7238f8312d5f45f6379dca448d649ef7653fe1ebfb1192866d866bccf(
    value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentSecurityPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bbdba23ac64476aa2d933e5304afe7622ff6a64c96dd0fd9615257f4b474f97(
    *,
    override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe355e99525e7c5ef166bcfc45e98afa5b1b584d8ffd7df99703207bb844cbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d0ddba646df337433d23d2e4a5ca721ba6caf4d3ce62a99a764bb38e13c028(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b7863798b074aeb578397885d9050514101a368d03ba16abbcee0e86da6832(
    value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigContentTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55424da847623d6cd9954ac56532cdc39c9073fd89bc5876824d7999f161ce34(
    *,
    frame_option: builtins.str,
    override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2247f930171b4babcece539255e36d394c7f924d730bca8a2bde2d9bfaf567c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc862645aea0a82b5125c87efdf3b528782874622e1f46186fa991a4af9a5a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9daa5cd2b24901b682ff1ef34dc7c9e43f4ad6d85ede776c73365f6212a265(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891ae2d798ff832a6a91476e6882e77834e350e791a58e6d7344d2fb6837d478(
    value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigFrameOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41853808f38b17f2521129fba0e3744ba7b2dfd822819e654c484398cdaadb6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43320dcb266475f0d7e02ab30a687386d941d60e0f7d8cb90df94e6fe4325dee(
    value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b89a201d947af795de0d14414b95ac25db86984938f9db4bcf09269e6b05d2c(
    *,
    override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    referrer_policy: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5722acdabf72d8340ead34ae0c3912a712e1a0b0560623b9deb37d9605d903(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938c831e883b6e02531a38d57309a5f48fcc3e4c55a7b063f40ee4e0b0c93a78(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f74f8161609c940a5a315187d274aa81020388aa6c5333e65d00e397b1a2ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39bf0fa1318b874d527daf761d71306f76229ce75f88963455dce5e805931565(
    value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigReferrerPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21181eac9b0a002b0c62197967127a8d2e926f3fda0d6e1d5b4fd63d90262df(
    *,
    access_control_max_age_sec: jsii.Number,
    override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    include_subdomains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    preload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea9ecc4e1f1c82f18c5450317afd7dd9594fb3a7363afc206b77915af57ab354(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1214cdc85e14ad808f3806fc59d30015e8b147c53243a0af9146b0fab97827(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c889086053f7a7f53601450448184217100f1755c48cb62745cf7f1438c267(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b28bb4c81503a692777cf72f8d4a1cdfdd46d867c8c76770a689e0b51d92024(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e87e6efb4441ca5554001c9863818a45de156ce666d3f678a830c0c01a55a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a046a019e850138ae3c71b4bd231d2ab8d33c2e9345ee053086cafd4df11967b(
    value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigStrictTransportSecurity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5b6c0fad6b0054d59632b0adbd9d356022c36aa9f6ba888f292f4645fc5fc8(
    *,
    override: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    protection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    mode_block: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    report_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f079c1338c91faf953c971388a691865fa76df29701ee1b84dd6551bb085cb97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5df3b832457b1fe2d3b9d797014a88bb7afa9f3dc0a138bcc4c2cc60595c00(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bd8bffe8fd51e252e65a088ee049bf669fd4d811f4a61109e11c59d0658422(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1386aa0a14ab45964e97b05e994918964b8df0b143c49cbe9d86e912bd18521c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049f7ffff746dd989d61c64e4dcf0c8db2e4d5b5740ebd0b0c386d779cb137af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a3aa3d74a2ad2132b8c944f6dfabba98f631df84b10d855810159659a717e3(
    value: typing.Optional[CloudfrontResponseHeadersPolicySecurityHeadersConfigXssProtection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9c6a2d5601796f69cf7b8698976ff23e55e932f1a7dd07ee7c0e83ccc26bf9(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    sampling_rate: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd961a1c09e691a73e5e2d41916ab27ecdbad80236f1a04fadf3ff8bbd8c0b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd2d1a17757c7c7f315bbcf817a0cfdf16dc44beec67b7468326483e39dcc30(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0a49b1757392f62a2ab95c85258f69948226ed2189022cd6583162dc4461a22(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3c03a7d18b2541970001cbb42068f81cbdb457553aa212dd20f58c5f869c6b(
    value: typing.Optional[CloudfrontResponseHeadersPolicyServerTimingHeadersConfig],
) -> None:
    """Type checking stubs"""
    pass
