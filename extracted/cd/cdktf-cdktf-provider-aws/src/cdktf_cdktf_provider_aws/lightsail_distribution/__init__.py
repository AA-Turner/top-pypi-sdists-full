r'''
# `aws_lightsail_distribution`

Refer to the Terraform Registry for docs: [`aws_lightsail_distribution`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution).
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


class LightsailDistribution(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistribution",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution aws_lightsail_distribution}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bundle_id: builtins.str,
        default_cache_behavior: typing.Union["LightsailDistributionDefaultCacheBehavior", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        origin: typing.Union["LightsailDistributionOrigin", typing.Dict[builtins.str, typing.Any]],
        cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LightsailDistributionCacheBehavior", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cache_behavior_settings: typing.Optional[typing.Union["LightsailDistributionCacheBehaviorSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LightsailDistributionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution aws_lightsail_distribution} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bundle_id: The bundle ID to use for the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#bundle_id LightsailDistribution#bundle_id}
        :param default_cache_behavior: default_cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#default_cache_behavior LightsailDistribution#default_cache_behavior}
        :param name: The name of the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#name LightsailDistribution#name}
        :param origin: origin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#origin LightsailDistribution#origin}
        :param cache_behavior: cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#cache_behavior LightsailDistribution#cache_behavior}
        :param cache_behavior_settings: cache_behavior_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#cache_behavior_settings LightsailDistribution#cache_behavior_settings}
        :param certificate_name: The name of the SSL/TLS certificate attached to the distribution, if any. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#certificate_name LightsailDistribution#certificate_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#id LightsailDistribution#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address_type: The IP address type of the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#ip_address_type LightsailDistribution#ip_address_type}
        :param is_enabled: Indicates whether the distribution is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#is_enabled LightsailDistribution#is_enabled}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#tags LightsailDistribution#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#tags_all LightsailDistribution#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#timeouts LightsailDistribution#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d39b704a950211a2aae91e800ee4185e4235bab248799bf8726603b725fd8f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LightsailDistributionConfig(
            bundle_id=bundle_id,
            default_cache_behavior=default_cache_behavior,
            name=name,
            origin=origin,
            cache_behavior=cache_behavior,
            cache_behavior_settings=cache_behavior_settings,
            certificate_name=certificate_name,
            id=id,
            ip_address_type=ip_address_type,
            is_enabled=is_enabled,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a LightsailDistribution resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LightsailDistribution to import.
        :param import_from_id: The id of the existing LightsailDistribution that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LightsailDistribution to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66147cf26aaea219fe9d3679b8f26c311e7f517a1e854113011a957404102d51)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCacheBehavior")
    def put_cache_behavior(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LightsailDistributionCacheBehavior", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df847331df9385767a04c1c5fc1877f13ee15199016a505b89340ca0e1c7eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCacheBehavior", [value]))

    @jsii.member(jsii_name="putCacheBehaviorSettings")
    def put_cache_behavior_settings(
        self,
        *,
        allowed_http_methods: typing.Optional[builtins.str] = None,
        cached_http_methods: typing.Optional[builtins.str] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        forwarded_cookies: typing.Optional[typing.Union["LightsailDistributionCacheBehaviorSettingsForwardedCookies", typing.Dict[builtins.str, typing.Any]]] = None,
        forwarded_headers: typing.Optional[typing.Union["LightsailDistributionCacheBehaviorSettingsForwardedHeaders", typing.Dict[builtins.str, typing.Any]]] = None,
        forwarded_query_strings: typing.Optional[typing.Union["LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_ttl: typing.Optional[jsii.Number] = None,
        minimum_ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allowed_http_methods: The HTTP methods that are processed and forwarded to the distribution's origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#allowed_http_methods LightsailDistribution#allowed_http_methods}
        :param cached_http_methods: The HTTP method responses that are cached by your distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#cached_http_methods LightsailDistribution#cached_http_methods}
        :param default_ttl: The default amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the content has been updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#default_ttl LightsailDistribution#default_ttl}
        :param forwarded_cookies: forwarded_cookies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#forwarded_cookies LightsailDistribution#forwarded_cookies}
        :param forwarded_headers: forwarded_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#forwarded_headers LightsailDistribution#forwarded_headers}
        :param forwarded_query_strings: forwarded_query_strings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#forwarded_query_strings LightsailDistribution#forwarded_query_strings}
        :param maximum_ttl: The maximum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#maximum_ttl LightsailDistribution#maximum_ttl}
        :param minimum_ttl: The minimum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#minimum_ttl LightsailDistribution#minimum_ttl}
        '''
        value = LightsailDistributionCacheBehaviorSettings(
            allowed_http_methods=allowed_http_methods,
            cached_http_methods=cached_http_methods,
            default_ttl=default_ttl,
            forwarded_cookies=forwarded_cookies,
            forwarded_headers=forwarded_headers,
            forwarded_query_strings=forwarded_query_strings,
            maximum_ttl=maximum_ttl,
            minimum_ttl=minimum_ttl,
        )

        return typing.cast(None, jsii.invoke(self, "putCacheBehaviorSettings", [value]))

    @jsii.member(jsii_name="putDefaultCacheBehavior")
    def put_default_cache_behavior(self, *, behavior: builtins.str) -> None:
        '''
        :param behavior: The cache behavior of the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#behavior LightsailDistribution#behavior}
        '''
        value = LightsailDistributionDefaultCacheBehavior(behavior=behavior)

        return typing.cast(None, jsii.invoke(self, "putDefaultCacheBehavior", [value]))

    @jsii.member(jsii_name="putOrigin")
    def put_origin(
        self,
        *,
        name: builtins.str,
        region_name: builtins.str,
        protocol_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the origin resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#name LightsailDistribution#name}
        :param region_name: The AWS Region name of the origin resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#region_name LightsailDistribution#region_name}
        :param protocol_policy: The protocol that your Amazon Lightsail distribution uses when establishing a connection with your origin to pull content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#protocol_policy LightsailDistribution#protocol_policy}
        '''
        value = LightsailDistributionOrigin(
            name=name, region_name=region_name, protocol_policy=protocol_policy
        )

        return typing.cast(None, jsii.invoke(self, "putOrigin", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#create LightsailDistribution#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#delete LightsailDistribution#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#update LightsailDistribution#update}.
        '''
        value = LightsailDistributionTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCacheBehavior")
    def reset_cache_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheBehavior", []))

    @jsii.member(jsii_name="resetCacheBehaviorSettings")
    def reset_cache_behavior_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheBehaviorSettings", []))

    @jsii.member(jsii_name="resetCertificateName")
    def reset_certificate_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpAddressType")
    def reset_ip_address_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddressType", []))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="alternativeDomainNames")
    def alternative_domain_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "alternativeDomainNames"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="cacheBehavior")
    def cache_behavior(self) -> "LightsailDistributionCacheBehaviorList":
        return typing.cast("LightsailDistributionCacheBehaviorList", jsii.get(self, "cacheBehavior"))

    @builtins.property
    @jsii.member(jsii_name="cacheBehaviorSettings")
    def cache_behavior_settings(
        self,
    ) -> "LightsailDistributionCacheBehaviorSettingsOutputReference":
        return typing.cast("LightsailDistributionCacheBehaviorSettingsOutputReference", jsii.get(self, "cacheBehaviorSettings"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="defaultCacheBehavior")
    def default_cache_behavior(
        self,
    ) -> "LightsailDistributionDefaultCacheBehaviorOutputReference":
        return typing.cast("LightsailDistributionDefaultCacheBehaviorOutputReference", jsii.get(self, "defaultCacheBehavior"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> "LightsailDistributionLocationList":
        return typing.cast("LightsailDistributionLocationList", jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="origin")
    def origin(self) -> "LightsailDistributionOriginOutputReference":
        return typing.cast("LightsailDistributionOriginOutputReference", jsii.get(self, "origin"))

    @builtins.property
    @jsii.member(jsii_name="originPublicDns")
    def origin_public_dns(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originPublicDns"))

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="supportCode")
    def support_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportCode"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "LightsailDistributionTimeoutsOutputReference":
        return typing.cast("LightsailDistributionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="bundleIdInput")
    def bundle_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bundleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheBehaviorInput")
    def cache_behavior_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LightsailDistributionCacheBehavior"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LightsailDistributionCacheBehavior"]]], jsii.get(self, "cacheBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheBehaviorSettingsInput")
    def cache_behavior_settings_input(
        self,
    ) -> typing.Optional["LightsailDistributionCacheBehaviorSettings"]:
        return typing.cast(typing.Optional["LightsailDistributionCacheBehaviorSettings"], jsii.get(self, "cacheBehaviorSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateNameInput")
    def certificate_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateNameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultCacheBehaviorInput")
    def default_cache_behavior_input(
        self,
    ) -> typing.Optional["LightsailDistributionDefaultCacheBehavior"]:
        return typing.cast(typing.Optional["LightsailDistributionDefaultCacheBehavior"], jsii.get(self, "defaultCacheBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressTypeInput")
    def ip_address_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="originInput")
    def origin_input(self) -> typing.Optional["LightsailDistributionOrigin"]:
        return typing.cast(typing.Optional["LightsailDistributionOrigin"], jsii.get(self, "originInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LightsailDistributionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LightsailDistributionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bundleId"))

    @bundle_id.setter
    def bundle_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53fb3e6d0da6f4c9ced2722f1e39463cccf0dbd4f03fa52c1e06bf1cac1daf44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificateName")
    def certificate_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateName"))

    @certificate_name.setter
    def certificate_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae63623d591b199fd6c8fdb6f849b63f6822374ae7d7cdf70f6a35cbf8b86b7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ef6c0253dbccf19b660117f049af295601021866f66e32ee9dde0fa8dcc590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressType"))

    @ip_address_type.setter
    def ip_address_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66219931230aa121cee8f61f1a3a5cb41ed4168722011a8267f4efedc0417ac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb6c3a659a477e582c80973e9057375c88f5f0f89e2727a4da8f8c6e44c21c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b12fc79b7bff00721daaa7268e06147e2d39d39c72176fc34167daf87d38cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__223b1718e08b623e0734a2b77ce32950473c4c4978794613ab14d02c8dbe6594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49a7260605258c45bb1b6ea71c56b45d559de32fa1b152901489e91cca1a2485)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionCacheBehavior",
    jsii_struct_bases=[],
    name_mapping={"behavior": "behavior", "path": "path"},
)
class LightsailDistributionCacheBehavior:
    def __init__(self, *, behavior: builtins.str, path: builtins.str) -> None:
        '''
        :param behavior: The cache behavior for the specified path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#behavior LightsailDistribution#behavior}
        :param path: The path to a directory or file to cached, or not cache. Use an asterisk symbol to specify wildcard directories (path/to/assets/*), and file types (*.html, *jpg, *js). Directories and file paths are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#path LightsailDistribution#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00659ec5e4cbdeae265f615342d800e7d6168564adaf4f05146bf46a5d52fa5)
            check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "behavior": behavior,
            "path": path,
        }

    @builtins.property
    def behavior(self) -> builtins.str:
        '''The cache behavior for the specified path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#behavior LightsailDistribution#behavior}
        '''
        result = self._values.get("behavior")
        assert result is not None, "Required property 'behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The path to a directory or file to cached, or not cache.

        Use an asterisk symbol to specify wildcard directories (path/to/assets/*), and file types (*.html, *jpg, *js). Directories and file paths are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#path LightsailDistribution#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionCacheBehavior(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionCacheBehaviorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7527750c4118570a0d9ba292c03e976460490580db673418578255fbafebce1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LightsailDistributionCacheBehaviorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb394c8c102a3472966fcb6aad153e1fc5db9dce5fa2262cb283f748f776e361)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LightsailDistributionCacheBehaviorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19ec80528f51077bc09005b1bdeff9bf3f092832f91bff04af5b72372e9c254)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68785b2d021d4fb9e6c271780a6f1b050f3439e90a90076a6af36ff4fa706ace)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56000b9cc3b70a0c753046d1020f433b4a042f48f2103077ba59fbd38fce2350)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LightsailDistributionCacheBehavior]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LightsailDistributionCacheBehavior]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LightsailDistributionCacheBehavior]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34664dea1f052308627e89a6fbe116a0f8a1613ca92905053341ab427ac44eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LightsailDistributionCacheBehaviorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22bf2fc211e2a8e9b2886a25874197306f2218250974eedf192e92a609de29ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="behaviorInput")
    def behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "behaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "behavior"))

    @behavior.setter
    def behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df8efd7fb0ed0ebe463468e1df3325fca299c17abce555b633d9a718c8e9226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b3bae3719757d662ee7c039281243fa7dab521cbde6c53d905ff02af8453889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionCacheBehavior]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionCacheBehavior]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionCacheBehavior]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__114c615c8d266fea68d17be41807adcf01d7308c3dd32c75120c50a7de13fe72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettings",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_http_methods": "allowedHttpMethods",
        "cached_http_methods": "cachedHttpMethods",
        "default_ttl": "defaultTtl",
        "forwarded_cookies": "forwardedCookies",
        "forwarded_headers": "forwardedHeaders",
        "forwarded_query_strings": "forwardedQueryStrings",
        "maximum_ttl": "maximumTtl",
        "minimum_ttl": "minimumTtl",
    },
)
class LightsailDistributionCacheBehaviorSettings:
    def __init__(
        self,
        *,
        allowed_http_methods: typing.Optional[builtins.str] = None,
        cached_http_methods: typing.Optional[builtins.str] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        forwarded_cookies: typing.Optional[typing.Union["LightsailDistributionCacheBehaviorSettingsForwardedCookies", typing.Dict[builtins.str, typing.Any]]] = None,
        forwarded_headers: typing.Optional[typing.Union["LightsailDistributionCacheBehaviorSettingsForwardedHeaders", typing.Dict[builtins.str, typing.Any]]] = None,
        forwarded_query_strings: typing.Optional[typing.Union["LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_ttl: typing.Optional[jsii.Number] = None,
        minimum_ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allowed_http_methods: The HTTP methods that are processed and forwarded to the distribution's origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#allowed_http_methods LightsailDistribution#allowed_http_methods}
        :param cached_http_methods: The HTTP method responses that are cached by your distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#cached_http_methods LightsailDistribution#cached_http_methods}
        :param default_ttl: The default amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the content has been updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#default_ttl LightsailDistribution#default_ttl}
        :param forwarded_cookies: forwarded_cookies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#forwarded_cookies LightsailDistribution#forwarded_cookies}
        :param forwarded_headers: forwarded_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#forwarded_headers LightsailDistribution#forwarded_headers}
        :param forwarded_query_strings: forwarded_query_strings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#forwarded_query_strings LightsailDistribution#forwarded_query_strings}
        :param maximum_ttl: The maximum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#maximum_ttl LightsailDistribution#maximum_ttl}
        :param minimum_ttl: The minimum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#minimum_ttl LightsailDistribution#minimum_ttl}
        '''
        if isinstance(forwarded_cookies, dict):
            forwarded_cookies = LightsailDistributionCacheBehaviorSettingsForwardedCookies(**forwarded_cookies)
        if isinstance(forwarded_headers, dict):
            forwarded_headers = LightsailDistributionCacheBehaviorSettingsForwardedHeaders(**forwarded_headers)
        if isinstance(forwarded_query_strings, dict):
            forwarded_query_strings = LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings(**forwarded_query_strings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f206596325dd5a37214d4a3ecd93e0248ca2243846b77f659029a315675af92)
            check_type(argname="argument allowed_http_methods", value=allowed_http_methods, expected_type=type_hints["allowed_http_methods"])
            check_type(argname="argument cached_http_methods", value=cached_http_methods, expected_type=type_hints["cached_http_methods"])
            check_type(argname="argument default_ttl", value=default_ttl, expected_type=type_hints["default_ttl"])
            check_type(argname="argument forwarded_cookies", value=forwarded_cookies, expected_type=type_hints["forwarded_cookies"])
            check_type(argname="argument forwarded_headers", value=forwarded_headers, expected_type=type_hints["forwarded_headers"])
            check_type(argname="argument forwarded_query_strings", value=forwarded_query_strings, expected_type=type_hints["forwarded_query_strings"])
            check_type(argname="argument maximum_ttl", value=maximum_ttl, expected_type=type_hints["maximum_ttl"])
            check_type(argname="argument minimum_ttl", value=minimum_ttl, expected_type=type_hints["minimum_ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_http_methods is not None:
            self._values["allowed_http_methods"] = allowed_http_methods
        if cached_http_methods is not None:
            self._values["cached_http_methods"] = cached_http_methods
        if default_ttl is not None:
            self._values["default_ttl"] = default_ttl
        if forwarded_cookies is not None:
            self._values["forwarded_cookies"] = forwarded_cookies
        if forwarded_headers is not None:
            self._values["forwarded_headers"] = forwarded_headers
        if forwarded_query_strings is not None:
            self._values["forwarded_query_strings"] = forwarded_query_strings
        if maximum_ttl is not None:
            self._values["maximum_ttl"] = maximum_ttl
        if minimum_ttl is not None:
            self._values["minimum_ttl"] = minimum_ttl

    @builtins.property
    def allowed_http_methods(self) -> typing.Optional[builtins.str]:
        '''The HTTP methods that are processed and forwarded to the distribution's origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#allowed_http_methods LightsailDistribution#allowed_http_methods}
        '''
        result = self._values.get("allowed_http_methods")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cached_http_methods(self) -> typing.Optional[builtins.str]:
        '''The HTTP method responses that are cached by your distribution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#cached_http_methods LightsailDistribution#cached_http_methods}
        '''
        result = self._values.get("cached_http_methods")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_ttl(self) -> typing.Optional[jsii.Number]:
        '''The default amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the content has been updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#default_ttl LightsailDistribution#default_ttl}
        '''
        result = self._values.get("default_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def forwarded_cookies(
        self,
    ) -> typing.Optional["LightsailDistributionCacheBehaviorSettingsForwardedCookies"]:
        '''forwarded_cookies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#forwarded_cookies LightsailDistribution#forwarded_cookies}
        '''
        result = self._values.get("forwarded_cookies")
        return typing.cast(typing.Optional["LightsailDistributionCacheBehaviorSettingsForwardedCookies"], result)

    @builtins.property
    def forwarded_headers(
        self,
    ) -> typing.Optional["LightsailDistributionCacheBehaviorSettingsForwardedHeaders"]:
        '''forwarded_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#forwarded_headers LightsailDistribution#forwarded_headers}
        '''
        result = self._values.get("forwarded_headers")
        return typing.cast(typing.Optional["LightsailDistributionCacheBehaviorSettingsForwardedHeaders"], result)

    @builtins.property
    def forwarded_query_strings(
        self,
    ) -> typing.Optional["LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings"]:
        '''forwarded_query_strings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#forwarded_query_strings LightsailDistribution#forwarded_query_strings}
        '''
        result = self._values.get("forwarded_query_strings")
        return typing.cast(typing.Optional["LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings"], result)

    @builtins.property
    def maximum_ttl(self) -> typing.Optional[jsii.Number]:
        '''The maximum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#maximum_ttl LightsailDistribution#maximum_ttl}
        '''
        result = self._values.get("maximum_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_ttl(self) -> typing.Optional[jsii.Number]:
        '''The minimum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#minimum_ttl LightsailDistribution#minimum_ttl}
        '''
        result = self._values.get("minimum_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionCacheBehaviorSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettingsForwardedCookies",
    jsii_struct_bases=[],
    name_mapping={"cookies_allow_list": "cookiesAllowList", "option": "option"},
)
class LightsailDistributionCacheBehaviorSettingsForwardedCookies:
    def __init__(
        self,
        *,
        cookies_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        option: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cookies_allow_list: The specific cookies to forward to your distribution's origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#cookies_allow_list LightsailDistribution#cookies_allow_list}
        :param option: Specifies which cookies to forward to the distribution's origin for a cache behavior: all, none, or allow-list to forward only the cookies specified in the cookiesAllowList parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895017f51ade2cb0f013a5221648c4cd0cb0eef7647774b24de64eeadf03ab05)
            check_type(argname="argument cookies_allow_list", value=cookies_allow_list, expected_type=type_hints["cookies_allow_list"])
            check_type(argname="argument option", value=option, expected_type=type_hints["option"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cookies_allow_list is not None:
            self._values["cookies_allow_list"] = cookies_allow_list
        if option is not None:
            self._values["option"] = option

    @builtins.property
    def cookies_allow_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The specific cookies to forward to your distribution's origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#cookies_allow_list LightsailDistribution#cookies_allow_list}
        '''
        result = self._values.get("cookies_allow_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def option(self) -> typing.Optional[builtins.str]:
        '''Specifies which cookies to forward to the distribution's origin for a cache behavior: all, none, or allow-list to forward only the cookies specified in the cookiesAllowList parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        '''
        result = self._values.get("option")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionCacheBehaviorSettingsForwardedCookies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionCacheBehaviorSettingsForwardedCookiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettingsForwardedCookiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b4b4cebaf9cc97b690f4d173619182417cd222e3d5480e2b4b2eb6bf729c211)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCookiesAllowList")
    def reset_cookies_allow_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCookiesAllowList", []))

    @jsii.member(jsii_name="resetOption")
    def reset_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOption", []))

    @builtins.property
    @jsii.member(jsii_name="cookiesAllowListInput")
    def cookies_allow_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cookiesAllowListInput"))

    @builtins.property
    @jsii.member(jsii_name="optionInput")
    def option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "optionInput"))

    @builtins.property
    @jsii.member(jsii_name="cookiesAllowList")
    def cookies_allow_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cookiesAllowList"))

    @cookies_allow_list.setter
    def cookies_allow_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e5b72a664474f2ef8e2d7112524d8b6a8e8ab00cd0da2e8a60f3d67ad71fbef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cookiesAllowList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="option")
    def option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "option"))

    @option.setter
    def option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ab6843439c7e13285c970cd4ca3e928d4c8178becfae342678bd0b863db860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "option", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedCookies]:
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedCookies], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedCookies],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f395bc04d0c7955c9be88318e72da31915ba3c7f2b25cf9a603b8e4836762ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettingsForwardedHeaders",
    jsii_struct_bases=[],
    name_mapping={"headers_allow_list": "headersAllowList", "option": "option"},
)
class LightsailDistributionCacheBehaviorSettingsForwardedHeaders:
    def __init__(
        self,
        *,
        headers_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        option: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param headers_allow_list: The specific headers to forward to your distribution's origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#headers_allow_list LightsailDistribution#headers_allow_list}
        :param option: The headers that you want your distribution to forward to your origin and base caching on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed5100db875df959d97b3357e1b3c11636e56f6dcc7566a6cd79161a3df17f61)
            check_type(argname="argument headers_allow_list", value=headers_allow_list, expected_type=type_hints["headers_allow_list"])
            check_type(argname="argument option", value=option, expected_type=type_hints["option"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if headers_allow_list is not None:
            self._values["headers_allow_list"] = headers_allow_list
        if option is not None:
            self._values["option"] = option

    @builtins.property
    def headers_allow_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The specific headers to forward to your distribution's origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#headers_allow_list LightsailDistribution#headers_allow_list}
        '''
        result = self._values.get("headers_allow_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def option(self) -> typing.Optional[builtins.str]:
        '''The headers that you want your distribution to forward to your origin and base caching on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        '''
        result = self._values.get("option")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionCacheBehaviorSettingsForwardedHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionCacheBehaviorSettingsForwardedHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettingsForwardedHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3916048b0b8110f95d4a54038c340e18ea928d99b20d7be19c41c1d6275ff47b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHeadersAllowList")
    def reset_headers_allow_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeadersAllowList", []))

    @jsii.member(jsii_name="resetOption")
    def reset_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOption", []))

    @builtins.property
    @jsii.member(jsii_name="headersAllowListInput")
    def headers_allow_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "headersAllowListInput"))

    @builtins.property
    @jsii.member(jsii_name="optionInput")
    def option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "optionInput"))

    @builtins.property
    @jsii.member(jsii_name="headersAllowList")
    def headers_allow_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "headersAllowList"))

    @headers_allow_list.setter
    def headers_allow_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee89436503f35c93a261a0aa25ac5794c47e59d82139418bd9255f948823d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headersAllowList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="option")
    def option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "option"))

    @option.setter
    def option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e06ffad3df522ca657f63026657828f00f19f017c8aa0eea3864fdd4088ad7ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "option", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedHeaders]:
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedHeaders], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedHeaders],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c4a5af6322a1a5c7a2a3682381878510e447891a1fdf980a1209ab2196fe88f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings",
    jsii_struct_bases=[],
    name_mapping={
        "option": "option",
        "query_strings_allowed_list": "queryStringsAllowedList",
    },
)
class LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings:
    def __init__(
        self,
        *,
        option: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_strings_allowed_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param option: Indicates whether the distribution forwards and caches based on query strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        :param query_strings_allowed_list: The specific query strings that the distribution forwards to the origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#query_strings_allowed_list LightsailDistribution#query_strings_allowed_list}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a9a6bdfa81463071226c6d6e0f5c1d7201a480ab495c838d655e1cf6c2cb2e0)
            check_type(argname="argument option", value=option, expected_type=type_hints["option"])
            check_type(argname="argument query_strings_allowed_list", value=query_strings_allowed_list, expected_type=type_hints["query_strings_allowed_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if option is not None:
            self._values["option"] = option
        if query_strings_allowed_list is not None:
            self._values["query_strings_allowed_list"] = query_strings_allowed_list

    @builtins.property
    def option(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the distribution forwards and caches based on query strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        '''
        result = self._values.get("option")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_strings_allowed_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The specific query strings that the distribution forwards to the origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#query_strings_allowed_list LightsailDistribution#query_strings_allowed_list}
        '''
        result = self._values.get("query_strings_allowed_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionCacheBehaviorSettingsForwardedQueryStringsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettingsForwardedQueryStringsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00f5e85f79f0a8b4f11fcca694d4f9167d361e4141a1bb571c64bc329eab6440)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOption")
    def reset_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOption", []))

    @jsii.member(jsii_name="resetQueryStringsAllowedList")
    def reset_query_strings_allowed_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringsAllowedList", []))

    @builtins.property
    @jsii.member(jsii_name="optionInput")
    def option_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optionInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringsAllowedListInput")
    def query_strings_allowed_list_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryStringsAllowedListInput"))

    @builtins.property
    @jsii.member(jsii_name="option")
    def option(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "option"))

    @option.setter
    def option(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37247c2f84c0fb536c879a822f0aa34752fad0582ad400e3bbe3c57faf844f2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "option", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringsAllowedList")
    def query_strings_allowed_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryStringsAllowedList"))

    @query_strings_allowed_list.setter
    def query_strings_allowed_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__144a47d5da2b1efc9bddc9f2b5de610e43981479005e718df9c6412795cecf64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringsAllowedList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings]:
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc115b868b84e74207e0a9fc92efcb1de2d8e731c49cdd558ac9da0110e36fce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LightsailDistributionCacheBehaviorSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__563227d44f8576cd93050bc112cd0c5c74a0b1753568266bbdada15203f5d613)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putForwardedCookies")
    def put_forwarded_cookies(
        self,
        *,
        cookies_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        option: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cookies_allow_list: The specific cookies to forward to your distribution's origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#cookies_allow_list LightsailDistribution#cookies_allow_list}
        :param option: Specifies which cookies to forward to the distribution's origin for a cache behavior: all, none, or allow-list to forward only the cookies specified in the cookiesAllowList parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        '''
        value = LightsailDistributionCacheBehaviorSettingsForwardedCookies(
            cookies_allow_list=cookies_allow_list, option=option
        )

        return typing.cast(None, jsii.invoke(self, "putForwardedCookies", [value]))

    @jsii.member(jsii_name="putForwardedHeaders")
    def put_forwarded_headers(
        self,
        *,
        headers_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        option: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param headers_allow_list: The specific headers to forward to your distribution's origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#headers_allow_list LightsailDistribution#headers_allow_list}
        :param option: The headers that you want your distribution to forward to your origin and base caching on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        '''
        value = LightsailDistributionCacheBehaviorSettingsForwardedHeaders(
            headers_allow_list=headers_allow_list, option=option
        )

        return typing.cast(None, jsii.invoke(self, "putForwardedHeaders", [value]))

    @jsii.member(jsii_name="putForwardedQueryStrings")
    def put_forwarded_query_strings(
        self,
        *,
        option: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_strings_allowed_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param option: Indicates whether the distribution forwards and caches based on query strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        :param query_strings_allowed_list: The specific query strings that the distribution forwards to the origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#query_strings_allowed_list LightsailDistribution#query_strings_allowed_list}
        '''
        value = LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings(
            option=option, query_strings_allowed_list=query_strings_allowed_list
        )

        return typing.cast(None, jsii.invoke(self, "putForwardedQueryStrings", [value]))

    @jsii.member(jsii_name="resetAllowedHttpMethods")
    def reset_allowed_http_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedHttpMethods", []))

    @jsii.member(jsii_name="resetCachedHttpMethods")
    def reset_cached_http_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCachedHttpMethods", []))

    @jsii.member(jsii_name="resetDefaultTtl")
    def reset_default_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTtl", []))

    @jsii.member(jsii_name="resetForwardedCookies")
    def reset_forwarded_cookies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardedCookies", []))

    @jsii.member(jsii_name="resetForwardedHeaders")
    def reset_forwarded_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardedHeaders", []))

    @jsii.member(jsii_name="resetForwardedQueryStrings")
    def reset_forwarded_query_strings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardedQueryStrings", []))

    @jsii.member(jsii_name="resetMaximumTtl")
    def reset_maximum_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumTtl", []))

    @jsii.member(jsii_name="resetMinimumTtl")
    def reset_minimum_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumTtl", []))

    @builtins.property
    @jsii.member(jsii_name="forwardedCookies")
    def forwarded_cookies(
        self,
    ) -> LightsailDistributionCacheBehaviorSettingsForwardedCookiesOutputReference:
        return typing.cast(LightsailDistributionCacheBehaviorSettingsForwardedCookiesOutputReference, jsii.get(self, "forwardedCookies"))

    @builtins.property
    @jsii.member(jsii_name="forwardedHeaders")
    def forwarded_headers(
        self,
    ) -> LightsailDistributionCacheBehaviorSettingsForwardedHeadersOutputReference:
        return typing.cast(LightsailDistributionCacheBehaviorSettingsForwardedHeadersOutputReference, jsii.get(self, "forwardedHeaders"))

    @builtins.property
    @jsii.member(jsii_name="forwardedQueryStrings")
    def forwarded_query_strings(
        self,
    ) -> LightsailDistributionCacheBehaviorSettingsForwardedQueryStringsOutputReference:
        return typing.cast(LightsailDistributionCacheBehaviorSettingsForwardedQueryStringsOutputReference, jsii.get(self, "forwardedQueryStrings"))

    @builtins.property
    @jsii.member(jsii_name="allowedHttpMethodsInput")
    def allowed_http_methods_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowedHttpMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="cachedHttpMethodsInput")
    def cached_http_methods_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cachedHttpMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTtlInput")
    def default_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardedCookiesInput")
    def forwarded_cookies_input(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedCookies]:
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedCookies], jsii.get(self, "forwardedCookiesInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardedHeadersInput")
    def forwarded_headers_input(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedHeaders]:
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedHeaders], jsii.get(self, "forwardedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardedQueryStringsInput")
    def forwarded_query_strings_input(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings]:
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings], jsii.get(self, "forwardedQueryStringsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumTtlInput")
    def maximum_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumTtlInput")
    def minimum_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedHttpMethods")
    def allowed_http_methods(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowedHttpMethods"))

    @allowed_http_methods.setter
    def allowed_http_methods(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e04dd03d0ec7ea3c8403dbdf3069940f5ccf901c4dfaf36e2177cb7121f18c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedHttpMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cachedHttpMethods")
    def cached_http_methods(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cachedHttpMethods"))

    @cached_http_methods.setter
    def cached_http_methods(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ccf3cb8289771ac340cbf9e8583bc03f032b0cfcd21da361e59d89c2a318109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cachedHttpMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2700e5fa55485cf8945d3df7982e250633ec95d020eeb41c9907320964d601c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumTtl")
    def maximum_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumTtl"))

    @maximum_ttl.setter
    def maximum_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c586a49dab424485bb78af3b62de85a4d42447ecdeeeb6dcceb69ab2da9fd9f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumTtl")
    def minimum_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumTtl"))

    @minimum_ttl.setter
    def minimum_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4bf10f7c9a2e9e2a5f1648d61a008cd2054ca84978d8dd9f07ae5c21060c085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettings]:
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LightsailDistributionCacheBehaviorSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__619f1d97e5fce3683573abb00fd390c2ed30387bc88db0f488e98ce7b480f951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bundle_id": "bundleId",
        "default_cache_behavior": "defaultCacheBehavior",
        "name": "name",
        "origin": "origin",
        "cache_behavior": "cacheBehavior",
        "cache_behavior_settings": "cacheBehaviorSettings",
        "certificate_name": "certificateName",
        "id": "id",
        "ip_address_type": "ipAddressType",
        "is_enabled": "isEnabled",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class LightsailDistributionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bundle_id: builtins.str,
        default_cache_behavior: typing.Union["LightsailDistributionDefaultCacheBehavior", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        origin: typing.Union["LightsailDistributionOrigin", typing.Dict[builtins.str, typing.Any]],
        cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LightsailDistributionCacheBehavior, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cache_behavior_settings: typing.Optional[typing.Union[LightsailDistributionCacheBehaviorSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        certificate_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LightsailDistributionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bundle_id: The bundle ID to use for the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#bundle_id LightsailDistribution#bundle_id}
        :param default_cache_behavior: default_cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#default_cache_behavior LightsailDistribution#default_cache_behavior}
        :param name: The name of the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#name LightsailDistribution#name}
        :param origin: origin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#origin LightsailDistribution#origin}
        :param cache_behavior: cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#cache_behavior LightsailDistribution#cache_behavior}
        :param cache_behavior_settings: cache_behavior_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#cache_behavior_settings LightsailDistribution#cache_behavior_settings}
        :param certificate_name: The name of the SSL/TLS certificate attached to the distribution, if any. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#certificate_name LightsailDistribution#certificate_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#id LightsailDistribution#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address_type: The IP address type of the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#ip_address_type LightsailDistribution#ip_address_type}
        :param is_enabled: Indicates whether the distribution is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#is_enabled LightsailDistribution#is_enabled}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#tags LightsailDistribution#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#tags_all LightsailDistribution#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#timeouts LightsailDistribution#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_cache_behavior, dict):
            default_cache_behavior = LightsailDistributionDefaultCacheBehavior(**default_cache_behavior)
        if isinstance(origin, dict):
            origin = LightsailDistributionOrigin(**origin)
        if isinstance(cache_behavior_settings, dict):
            cache_behavior_settings = LightsailDistributionCacheBehaviorSettings(**cache_behavior_settings)
        if isinstance(timeouts, dict):
            timeouts = LightsailDistributionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0373eafb8660792800c244f71ea3e533260b83f809be7bad67ac3a81c8282bb6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument default_cache_behavior", value=default_cache_behavior, expected_type=type_hints["default_cache_behavior"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            check_type(argname="argument cache_behavior", value=cache_behavior, expected_type=type_hints["cache_behavior"])
            check_type(argname="argument cache_behavior_settings", value=cache_behavior_settings, expected_type=type_hints["cache_behavior_settings"])
            check_type(argname="argument certificate_name", value=certificate_name, expected_type=type_hints["certificate_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bundle_id": bundle_id,
            "default_cache_behavior": default_cache_behavior,
            "name": name,
            "origin": origin,
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
        if cache_behavior is not None:
            self._values["cache_behavior"] = cache_behavior
        if cache_behavior_settings is not None:
            self._values["cache_behavior_settings"] = cache_behavior_settings
        if certificate_name is not None:
            self._values["certificate_name"] = certificate_name
        if id is not None:
            self._values["id"] = id
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
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
    def bundle_id(self) -> builtins.str:
        '''The bundle ID to use for the distribution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#bundle_id LightsailDistribution#bundle_id}
        '''
        result = self._values.get("bundle_id")
        assert result is not None, "Required property 'bundle_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_cache_behavior(self) -> "LightsailDistributionDefaultCacheBehavior":
        '''default_cache_behavior block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#default_cache_behavior LightsailDistribution#default_cache_behavior}
        '''
        result = self._values.get("default_cache_behavior")
        assert result is not None, "Required property 'default_cache_behavior' is missing"
        return typing.cast("LightsailDistributionDefaultCacheBehavior", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the distribution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#name LightsailDistribution#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin(self) -> "LightsailDistributionOrigin":
        '''origin block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#origin LightsailDistribution#origin}
        '''
        result = self._values.get("origin")
        assert result is not None, "Required property 'origin' is missing"
        return typing.cast("LightsailDistributionOrigin", result)

    @builtins.property
    def cache_behavior(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LightsailDistributionCacheBehavior]]]:
        '''cache_behavior block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#cache_behavior LightsailDistribution#cache_behavior}
        '''
        result = self._values.get("cache_behavior")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LightsailDistributionCacheBehavior]]], result)

    @builtins.property
    def cache_behavior_settings(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettings]:
        '''cache_behavior_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#cache_behavior_settings LightsailDistribution#cache_behavior_settings}
        '''
        result = self._values.get("cache_behavior_settings")
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettings], result)

    @builtins.property
    def certificate_name(self) -> typing.Optional[builtins.str]:
        '''The name of the SSL/TLS certificate attached to the distribution, if any.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#certificate_name LightsailDistribution#certificate_name}
        '''
        result = self._values.get("certificate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#id LightsailDistribution#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''The IP address type of the distribution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#ip_address_type LightsailDistribution#ip_address_type}
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the distribution is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#is_enabled LightsailDistribution#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#tags LightsailDistribution#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#tags_all LightsailDistribution#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["LightsailDistributionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#timeouts LightsailDistribution#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LightsailDistributionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionDefaultCacheBehavior",
    jsii_struct_bases=[],
    name_mapping={"behavior": "behavior"},
)
class LightsailDistributionDefaultCacheBehavior:
    def __init__(self, *, behavior: builtins.str) -> None:
        '''
        :param behavior: The cache behavior of the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#behavior LightsailDistribution#behavior}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b1879da353fc0e2b01baab54d14cc24774f2421a48b25b9b88987ab048675a6)
            check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "behavior": behavior,
        }

    @builtins.property
    def behavior(self) -> builtins.str:
        '''The cache behavior of the distribution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#behavior LightsailDistribution#behavior}
        '''
        result = self._values.get("behavior")
        assert result is not None, "Required property 'behavior' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionDefaultCacheBehavior(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionDefaultCacheBehaviorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionDefaultCacheBehaviorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c843836323d45f5bcbbdec335067e1c6e1fbeba2476ce8033f22c47706743af1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="behaviorInput")
    def behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "behaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "behavior"))

    @behavior.setter
    def behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6908b2e0cebe2147497563ea5ec6142389713d4e0db16be4c550466a853ef43e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LightsailDistributionDefaultCacheBehavior]:
        return typing.cast(typing.Optional[LightsailDistributionDefaultCacheBehavior], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LightsailDistributionDefaultCacheBehavior],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6426b22139a1e9d84270df741a3b4806c99a8ff50d0761726f17123fc531474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionLocation",
    jsii_struct_bases=[],
    name_mapping={},
)
class LightsailDistributionLocation:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionLocationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionLocationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__901d39e17a307c7ff0806d524594174a69081c882a2ef4915259722ae5b8ea9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LightsailDistributionLocationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__151b4a9e83c34be594473202073752f9fa30194ef656a76061f4806ae45f1d9e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LightsailDistributionLocationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b0b755c95094cfef67792d2bc6d626cc5e28491466f3309ba71513636d1b392)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3449ed9c199ba181dd3303e2379552961685029b9cbef71361fb02dd550eacc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e84cb44ef833bea4faa8eea39886dd34467e932bded3b31e66e01ff010cef4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LightsailDistributionLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49ca969d1d09e00845af23b4f1143dde64cfd4941ce52a52fee6c351cd3c9378)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @builtins.property
    @jsii.member(jsii_name="regionName")
    def region_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LightsailDistributionLocation]:
        return typing.cast(typing.Optional[LightsailDistributionLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LightsailDistributionLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f375e7ac0ca667a48be2190bfe1e3559e022e0f249bbf997e16609d5186126d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionOrigin",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "region_name": "regionName",
        "protocol_policy": "protocolPolicy",
    },
)
class LightsailDistributionOrigin:
    def __init__(
        self,
        *,
        name: builtins.str,
        region_name: builtins.str,
        protocol_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the origin resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#name LightsailDistribution#name}
        :param region_name: The AWS Region name of the origin resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#region_name LightsailDistribution#region_name}
        :param protocol_policy: The protocol that your Amazon Lightsail distribution uses when establishing a connection with your origin to pull content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#protocol_policy LightsailDistribution#protocol_policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca586090d3d4a01fa6ddb9f46b59a648559366fbac198325b50e6157305849a9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            check_type(argname="argument protocol_policy", value=protocol_policy, expected_type=type_hints["protocol_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "region_name": region_name,
        }
        if protocol_policy is not None:
            self._values["protocol_policy"] = protocol_policy

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the origin resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#name LightsailDistribution#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region_name(self) -> builtins.str:
        '''The AWS Region name of the origin resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#region_name LightsailDistribution#region_name}
        '''
        result = self._values.get("region_name")
        assert result is not None, "Required property 'region_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol_policy(self) -> typing.Optional[builtins.str]:
        '''The protocol that your Amazon Lightsail distribution uses when establishing a connection with your origin to pull content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#protocol_policy LightsailDistribution#protocol_policy}
        '''
        result = self._values.get("protocol_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionOrigin(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionOriginOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionOriginOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84d820c7f726bb17e6996bed861dc8e280c6b2fbdfae0b72e64067415ababb62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProtocolPolicy")
    def reset_protocol_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocolPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolPolicyInput")
    def protocol_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="regionNameInput")
    def region_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f0a31b6656b882039341f2a89d2bc8a703dd34bab21fc9e9f10dc49394d966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocolPolicy")
    def protocol_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocolPolicy"))

    @protocol_policy.setter
    def protocol_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0dd1d2b4fbf2ebbc1b241a2c42453be9f735c8d31d4a8514046fdd5d4a63ef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionName")
    def region_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionName"))

    @region_name.setter
    def region_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b56ac1ce15c1a351aac91ece06c23a2a570e6ada15c266e2be72b93cc4b80a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LightsailDistributionOrigin]:
        return typing.cast(typing.Optional[LightsailDistributionOrigin], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LightsailDistributionOrigin],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9135708947f72b4c37b11d6d9209eadb0799173885b0d7a6d075c664579b0c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class LightsailDistributionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#create LightsailDistribution#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#delete LightsailDistribution#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#update LightsailDistribution#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f4377ff43944f15885315c1d35a915917afee75b4f9d5c129fe1f7da1cad464)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#create LightsailDistribution#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#delete LightsailDistribution#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/lightsail_distribution#update LightsailDistribution#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.lightsailDistribution.LightsailDistributionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbb65dbfaac2121ff6e2a746851630f48b5910b4298a248642a509e021b49bca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c086b93f940a54ed49a80de47154ebcb9103bb993f3129441769a37de104d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a06fd3069affc79c74b4b68e0b82d0a710f266f07bea458efc47a54c67a3eda3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c7f506156c58b6e91230c5225fdb74aedfb324e279c0150460d1020b06b08ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0577e3952bcae0ce46e2e94deeb4139b83f412a56d49a8f5b7b7c919c6e2c566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LightsailDistribution",
    "LightsailDistributionCacheBehavior",
    "LightsailDistributionCacheBehaviorList",
    "LightsailDistributionCacheBehaviorOutputReference",
    "LightsailDistributionCacheBehaviorSettings",
    "LightsailDistributionCacheBehaviorSettingsForwardedCookies",
    "LightsailDistributionCacheBehaviorSettingsForwardedCookiesOutputReference",
    "LightsailDistributionCacheBehaviorSettingsForwardedHeaders",
    "LightsailDistributionCacheBehaviorSettingsForwardedHeadersOutputReference",
    "LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings",
    "LightsailDistributionCacheBehaviorSettingsForwardedQueryStringsOutputReference",
    "LightsailDistributionCacheBehaviorSettingsOutputReference",
    "LightsailDistributionConfig",
    "LightsailDistributionDefaultCacheBehavior",
    "LightsailDistributionDefaultCacheBehaviorOutputReference",
    "LightsailDistributionLocation",
    "LightsailDistributionLocationList",
    "LightsailDistributionLocationOutputReference",
    "LightsailDistributionOrigin",
    "LightsailDistributionOriginOutputReference",
    "LightsailDistributionTimeouts",
    "LightsailDistributionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b7d39b704a950211a2aae91e800ee4185e4235bab248799bf8726603b725fd8f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bundle_id: builtins.str,
    default_cache_behavior: typing.Union[LightsailDistributionDefaultCacheBehavior, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    origin: typing.Union[LightsailDistributionOrigin, typing.Dict[builtins.str, typing.Any]],
    cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LightsailDistributionCacheBehavior, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cache_behavior_settings: typing.Optional[typing.Union[LightsailDistributionCacheBehaviorSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LightsailDistributionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__66147cf26aaea219fe9d3679b8f26c311e7f517a1e854113011a957404102d51(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df847331df9385767a04c1c5fc1877f13ee15199016a505b89340ca0e1c7eb6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LightsailDistributionCacheBehavior, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fb3e6d0da6f4c9ced2722f1e39463cccf0dbd4f03fa52c1e06bf1cac1daf44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae63623d591b199fd6c8fdb6f849b63f6822374ae7d7cdf70f6a35cbf8b86b7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ef6c0253dbccf19b660117f049af295601021866f66e32ee9dde0fa8dcc590(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66219931230aa121cee8f61f1a3a5cb41ed4168722011a8267f4efedc0417ac6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb6c3a659a477e582c80973e9057375c88f5f0f89e2727a4da8f8c6e44c21c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b12fc79b7bff00721daaa7268e06147e2d39d39c72176fc34167daf87d38cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__223b1718e08b623e0734a2b77ce32950473c4c4978794613ab14d02c8dbe6594(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49a7260605258c45bb1b6ea71c56b45d559de32fa1b152901489e91cca1a2485(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00659ec5e4cbdeae265f615342d800e7d6168564adaf4f05146bf46a5d52fa5(
    *,
    behavior: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7527750c4118570a0d9ba292c03e976460490580db673418578255fbafebce1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb394c8c102a3472966fcb6aad153e1fc5db9dce5fa2262cb283f748f776e361(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19ec80528f51077bc09005b1bdeff9bf3f092832f91bff04af5b72372e9c254(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68785b2d021d4fb9e6c271780a6f1b050f3439e90a90076a6af36ff4fa706ace(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56000b9cc3b70a0c753046d1020f433b4a042f48f2103077ba59fbd38fce2350(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34664dea1f052308627e89a6fbe116a0f8a1613ca92905053341ab427ac44eea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LightsailDistributionCacheBehavior]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22bf2fc211e2a8e9b2886a25874197306f2218250974eedf192e92a609de29ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df8efd7fb0ed0ebe463468e1df3325fca299c17abce555b633d9a718c8e9226(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3bae3719757d662ee7c039281243fa7dab521cbde6c53d905ff02af8453889(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114c615c8d266fea68d17be41807adcf01d7308c3dd32c75120c50a7de13fe72(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionCacheBehavior]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f206596325dd5a37214d4a3ecd93e0248ca2243846b77f659029a315675af92(
    *,
    allowed_http_methods: typing.Optional[builtins.str] = None,
    cached_http_methods: typing.Optional[builtins.str] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    forwarded_cookies: typing.Optional[typing.Union[LightsailDistributionCacheBehaviorSettingsForwardedCookies, typing.Dict[builtins.str, typing.Any]]] = None,
    forwarded_headers: typing.Optional[typing.Union[LightsailDistributionCacheBehaviorSettingsForwardedHeaders, typing.Dict[builtins.str, typing.Any]]] = None,
    forwarded_query_strings: typing.Optional[typing.Union[LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_ttl: typing.Optional[jsii.Number] = None,
    minimum_ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895017f51ade2cb0f013a5221648c4cd0cb0eef7647774b24de64eeadf03ab05(
    *,
    cookies_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    option: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4b4cebaf9cc97b690f4d173619182417cd222e3d5480e2b4b2eb6bf729c211(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5b72a664474f2ef8e2d7112524d8b6a8e8ab00cd0da2e8a60f3d67ad71fbef(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ab6843439c7e13285c970cd4ca3e928d4c8178becfae342678bd0b863db860(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f395bc04d0c7955c9be88318e72da31915ba3c7f2b25cf9a603b8e4836762ea(
    value: typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedCookies],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5100db875df959d97b3357e1b3c11636e56f6dcc7566a6cd79161a3df17f61(
    *,
    headers_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    option: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3916048b0b8110f95d4a54038c340e18ea928d99b20d7be19c41c1d6275ff47b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee89436503f35c93a261a0aa25ac5794c47e59d82139418bd9255f948823d27(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06ffad3df522ca657f63026657828f00f19f017c8aa0eea3864fdd4088ad7ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4a5af6322a1a5c7a2a3682381878510e447891a1fdf980a1209ab2196fe88f(
    value: typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedHeaders],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9a6bdfa81463071226c6d6e0f5c1d7201a480ab495c838d655e1cf6c2cb2e0(
    *,
    option: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_strings_allowed_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f5e85f79f0a8b4f11fcca694d4f9167d361e4141a1bb571c64bc329eab6440(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37247c2f84c0fb536c879a822f0aa34752fad0582ad400e3bbe3c57faf844f2f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144a47d5da2b1efc9bddc9f2b5de610e43981479005e718df9c6412795cecf64(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc115b868b84e74207e0a9fc92efcb1de2d8e731c49cdd558ac9da0110e36fce(
    value: typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__563227d44f8576cd93050bc112cd0c5c74a0b1753568266bbdada15203f5d613(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e04dd03d0ec7ea3c8403dbdf3069940f5ccf901c4dfaf36e2177cb7121f18c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ccf3cb8289771ac340cbf9e8583bc03f032b0cfcd21da361e59d89c2a318109(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2700e5fa55485cf8945d3df7982e250633ec95d020eeb41c9907320964d601c6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c586a49dab424485bb78af3b62de85a4d42447ecdeeeb6dcceb69ab2da9fd9f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4bf10f7c9a2e9e2a5f1648d61a008cd2054ca84978d8dd9f07ae5c21060c085(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619f1d97e5fce3683573abb00fd390c2ed30387bc88db0f488e98ce7b480f951(
    value: typing.Optional[LightsailDistributionCacheBehaviorSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0373eafb8660792800c244f71ea3e533260b83f809be7bad67ac3a81c8282bb6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bundle_id: builtins.str,
    default_cache_behavior: typing.Union[LightsailDistributionDefaultCacheBehavior, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    origin: typing.Union[LightsailDistributionOrigin, typing.Dict[builtins.str, typing.Any]],
    cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LightsailDistributionCacheBehavior, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cache_behavior_settings: typing.Optional[typing.Union[LightsailDistributionCacheBehaviorSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LightsailDistributionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b1879da353fc0e2b01baab54d14cc24774f2421a48b25b9b88987ab048675a6(
    *,
    behavior: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c843836323d45f5bcbbdec335067e1c6e1fbeba2476ce8033f22c47706743af1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6908b2e0cebe2147497563ea5ec6142389713d4e0db16be4c550466a853ef43e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6426b22139a1e9d84270df741a3b4806c99a8ff50d0761726f17123fc531474(
    value: typing.Optional[LightsailDistributionDefaultCacheBehavior],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901d39e17a307c7ff0806d524594174a69081c882a2ef4915259722ae5b8ea9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151b4a9e83c34be594473202073752f9fa30194ef656a76061f4806ae45f1d9e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b0b755c95094cfef67792d2bc6d626cc5e28491466f3309ba71513636d1b392(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3449ed9c199ba181dd3303e2379552961685029b9cbef71361fb02dd550eacc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e84cb44ef833bea4faa8eea39886dd34467e932bded3b31e66e01ff010cef4e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ca969d1d09e00845af23b4f1143dde64cfd4941ce52a52fee6c351cd3c9378(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f375e7ac0ca667a48be2190bfe1e3559e022e0f249bbf997e16609d5186126d5(
    value: typing.Optional[LightsailDistributionLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca586090d3d4a01fa6ddb9f46b59a648559366fbac198325b50e6157305849a9(
    *,
    name: builtins.str,
    region_name: builtins.str,
    protocol_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d820c7f726bb17e6996bed861dc8e280c6b2fbdfae0b72e64067415ababb62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f0a31b6656b882039341f2a89d2bc8a703dd34bab21fc9e9f10dc49394d966(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0dd1d2b4fbf2ebbc1b241a2c42453be9f735c8d31d4a8514046fdd5d4a63ef8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b56ac1ce15c1a351aac91ece06c23a2a570e6ada15c266e2be72b93cc4b80a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9135708947f72b4c37b11d6d9209eadb0799173885b0d7a6d075c664579b0c3(
    value: typing.Optional[LightsailDistributionOrigin],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4377ff43944f15885315c1d35a915917afee75b4f9d5c129fe1f7da1cad464(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbb65dbfaac2121ff6e2a746851630f48b5910b4298a248642a509e021b49bca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c086b93f940a54ed49a80de47154ebcb9103bb993f3129441769a37de104d1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06fd3069affc79c74b4b68e0b82d0a710f266f07bea458efc47a54c67a3eda3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7f506156c58b6e91230c5225fdb74aedfb324e279c0150460d1020b06b08ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0577e3952bcae0ce46e2e94deeb4139b83f412a56d49a8f5b7b7c919c6e2c566(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
