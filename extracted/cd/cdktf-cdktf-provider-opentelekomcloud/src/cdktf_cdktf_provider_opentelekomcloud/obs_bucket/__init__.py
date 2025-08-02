r'''
# `opentelekomcloud_obs_bucket`

Refer to the Terraform Registry for docs: [`opentelekomcloud_obs_bucket`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket).
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


class ObsBucket(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucket",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket opentelekomcloud_obs_bucket}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bucket: builtins.str,
        acl: typing.Optional[builtins.str] = None,
        cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketCorsRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_notifications: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketEventNotifications", typing.Dict[builtins.str, typing.Any]]]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketLifecycleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        logging: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketLogging", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parallel_fs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        server_side_encryption: typing.Optional[typing.Union["ObsBucketServerSideEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_class: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        versioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        website: typing.Optional[typing.Union["ObsBucketWebsite", typing.Dict[builtins.str, typing.Any]]] = None,
        worm_policy: typing.Optional[typing.Union["ObsBucketWormPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket opentelekomcloud_obs_bucket} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#bucket ObsBucket#bucket}.
        :param acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#acl ObsBucket#acl}.
        :param cors_rule: cors_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#cors_rule ObsBucket#cors_rule}
        :param event_notifications: event_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#event_notifications ObsBucket#event_notifications}
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#force_destroy ObsBucket#force_destroy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#id ObsBucket#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lifecycle_rule: lifecycle_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#lifecycle_rule ObsBucket#lifecycle_rule}
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#logging ObsBucket#logging}
        :param parallel_fs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#parallel_fs ObsBucket#parallel_fs}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#region ObsBucket#region}.
        :param server_side_encryption: server_side_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#server_side_encryption ObsBucket#server_side_encryption}
        :param storage_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#storage_class ObsBucket#storage_class}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#tags ObsBucket#tags}.
        :param user_domain_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#user_domain_names ObsBucket#user_domain_names}.
        :param versioning: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#versioning ObsBucket#versioning}.
        :param website: website block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#website ObsBucket#website}
        :param worm_policy: worm_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#worm_policy ObsBucket#worm_policy}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d6614c59b8ea0d96dad0c1d6dde0756436ef254a4d38d5c41df70b47d070c71)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ObsBucketConfig(
            bucket=bucket,
            acl=acl,
            cors_rule=cors_rule,
            event_notifications=event_notifications,
            force_destroy=force_destroy,
            id=id,
            lifecycle_rule=lifecycle_rule,
            logging=logging,
            parallel_fs=parallel_fs,
            region=region,
            server_side_encryption=server_side_encryption,
            storage_class=storage_class,
            tags=tags,
            user_domain_names=user_domain_names,
            versioning=versioning,
            website=website,
            worm_policy=worm_policy,
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
        '''Generates CDKTF code for importing a ObsBucket resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ObsBucket to import.
        :param import_from_id: The id of the existing ObsBucket that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ObsBucket to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73336310d79043ca4eee1cf681341c7abba4a8b78ecd4e37a1cde9630e892251)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCorsRule")
    def put_cors_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketCorsRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd750a90c7aead9e48f2e0304af03b6fc8326e66779020b0edb81b1c693675e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCorsRule", [value]))

    @jsii.member(jsii_name="putEventNotifications")
    def put_event_notifications(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketEventNotifications", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e3e91a76189732f19bc9467cdf14cd21cc8eff84ca5d5376426d0766320292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEventNotifications", [value]))

    @jsii.member(jsii_name="putLifecycleRule")
    def put_lifecycle_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketLifecycleRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1980a1c652b8a3c196fde5215b949c9c357b8e4160a766c9be8f595517636748)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLifecycleRule", [value]))

    @jsii.member(jsii_name="putLogging")
    def put_logging(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketLogging", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f90561b1d322b870d758571ec56cf1b4f4758a1344f21c7c6a5693f39c2549f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogging", [value]))

    @jsii.member(jsii_name="putServerSideEncryption")
    def put_server_side_encryption(
        self,
        *,
        algorithm: builtins.str,
        kms_key_id: builtins.str,
        kms_project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#algorithm ObsBucket#algorithm}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#kms_key_id ObsBucket#kms_key_id}.
        :param kms_project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#kms_project_id ObsBucket#kms_project_id}.
        '''
        value = ObsBucketServerSideEncryption(
            algorithm=algorithm, kms_key_id=kms_key_id, kms_project_id=kms_project_id
        )

        return typing.cast(None, jsii.invoke(self, "putServerSideEncryption", [value]))

    @jsii.member(jsii_name="putWebsite")
    def put_website(
        self,
        *,
        error_document: typing.Optional[builtins.str] = None,
        index_document: typing.Optional[builtins.str] = None,
        redirect_all_requests_to: typing.Optional[builtins.str] = None,
        routing_rules: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param error_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#error_document ObsBucket#error_document}.
        :param index_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#index_document ObsBucket#index_document}.
        :param redirect_all_requests_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#redirect_all_requests_to ObsBucket#redirect_all_requests_to}.
        :param routing_rules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#routing_rules ObsBucket#routing_rules}.
        '''
        value = ObsBucketWebsite(
            error_document=error_document,
            index_document=index_document,
            redirect_all_requests_to=redirect_all_requests_to,
            routing_rules=routing_rules,
        )

        return typing.cast(None, jsii.invoke(self, "putWebsite", [value]))

    @jsii.member(jsii_name="putWormPolicy")
    def put_worm_policy(
        self,
        *,
        days: typing.Optional[jsii.Number] = None,
        years: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#days ObsBucket#days}.
        :param years: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#years ObsBucket#years}.
        '''
        value = ObsBucketWormPolicy(days=days, years=years)

        return typing.cast(None, jsii.invoke(self, "putWormPolicy", [value]))

    @jsii.member(jsii_name="resetAcl")
    def reset_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcl", []))

    @jsii.member(jsii_name="resetCorsRule")
    def reset_cors_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCorsRule", []))

    @jsii.member(jsii_name="resetEventNotifications")
    def reset_event_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventNotifications", []))

    @jsii.member(jsii_name="resetForceDestroy")
    def reset_force_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDestroy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLifecycleRule")
    def reset_lifecycle_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleRule", []))

    @jsii.member(jsii_name="resetLogging")
    def reset_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogging", []))

    @jsii.member(jsii_name="resetParallelFs")
    def reset_parallel_fs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelFs", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetServerSideEncryption")
    def reset_server_side_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerSideEncryption", []))

    @jsii.member(jsii_name="resetStorageClass")
    def reset_storage_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageClass", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetUserDomainNames")
    def reset_user_domain_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDomainNames", []))

    @jsii.member(jsii_name="resetVersioning")
    def reset_versioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersioning", []))

    @jsii.member(jsii_name="resetWebsite")
    def reset_website(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebsite", []))

    @jsii.member(jsii_name="resetWormPolicy")
    def reset_worm_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWormPolicy", []))

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
    @jsii.member(jsii_name="bucketDomainName")
    def bucket_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketDomainName"))

    @builtins.property
    @jsii.member(jsii_name="bucketVersion")
    def bucket_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketVersion"))

    @builtins.property
    @jsii.member(jsii_name="corsRule")
    def cors_rule(self) -> "ObsBucketCorsRuleList":
        return typing.cast("ObsBucketCorsRuleList", jsii.get(self, "corsRule"))

    @builtins.property
    @jsii.member(jsii_name="eventNotifications")
    def event_notifications(self) -> "ObsBucketEventNotificationsList":
        return typing.cast("ObsBucketEventNotificationsList", jsii.get(self, "eventNotifications"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleRule")
    def lifecycle_rule(self) -> "ObsBucketLifecycleRuleList":
        return typing.cast("ObsBucketLifecycleRuleList", jsii.get(self, "lifecycleRule"))

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> "ObsBucketLoggingList":
        return typing.cast("ObsBucketLoggingList", jsii.get(self, "logging"))

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryption")
    def server_side_encryption(self) -> "ObsBucketServerSideEncryptionOutputReference":
        return typing.cast("ObsBucketServerSideEncryptionOutputReference", jsii.get(self, "serverSideEncryption"))

    @builtins.property
    @jsii.member(jsii_name="website")
    def website(self) -> "ObsBucketWebsiteOutputReference":
        return typing.cast("ObsBucketWebsiteOutputReference", jsii.get(self, "website"))

    @builtins.property
    @jsii.member(jsii_name="wormPolicy")
    def worm_policy(self) -> "ObsBucketWormPolicyOutputReference":
        return typing.cast("ObsBucketWormPolicyOutputReference", jsii.get(self, "wormPolicy"))

    @builtins.property
    @jsii.member(jsii_name="aclInput")
    def acl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aclInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="corsRuleInput")
    def cors_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketCorsRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketCorsRule"]]], jsii.get(self, "corsRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="eventNotificationsInput")
    def event_notifications_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketEventNotifications"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketEventNotifications"]]], jsii.get(self, "eventNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDestroyInput")
    def force_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleRuleInput")
    def lifecycle_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRule"]]], jsii.get(self, "lifecycleRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLogging"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLogging"]]], jsii.get(self, "loggingInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelFsInput")
    def parallel_fs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "parallelFsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionInput")
    def server_side_encryption_input(
        self,
    ) -> typing.Optional["ObsBucketServerSideEncryption"]:
        return typing.cast(typing.Optional["ObsBucketServerSideEncryption"], jsii.get(self, "serverSideEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="storageClassInput")
    def storage_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="userDomainNamesInput")
    def user_domain_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userDomainNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="versioningInput")
    def versioning_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "versioningInput"))

    @builtins.property
    @jsii.member(jsii_name="websiteInput")
    def website_input(self) -> typing.Optional["ObsBucketWebsite"]:
        return typing.cast(typing.Optional["ObsBucketWebsite"], jsii.get(self, "websiteInput"))

    @builtins.property
    @jsii.member(jsii_name="wormPolicyInput")
    def worm_policy_input(self) -> typing.Optional["ObsBucketWormPolicy"]:
        return typing.cast(typing.Optional["ObsBucketWormPolicy"], jsii.get(self, "wormPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="acl")
    def acl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acl"))

    @acl.setter
    def acl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d9404cbf6d9954421f230f4526740eca919037f90531b2bda4f25bc2f01fbdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12aecb0bba794527e0211533fc9c9a5cec8c1a084ea3e7ca82ca4720d079cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceDestroy")
    def force_destroy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDestroy"))

    @force_destroy.setter
    def force_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b470f43269c293cd8b342666d66badc8c4ba5210ba6001b7f7261701fed78516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ea99a6dd45c5c3a3991c9fa3327deeeb3acfd0ce799034a89fbfca98137fb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelFs")
    def parallel_fs(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "parallelFs"))

    @parallel_fs.setter
    def parallel_fs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2913dfeac99d6b28d5f87deb2012b9131ed2ad8601fb243611898a76a5fdbf50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelFs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff96e25e196e1d8211303075e6b9134eccd7812257def1bc26e15348f8280ed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af52c3e2cd190e1de26ac1c0fd1f7eeef284268f187773e71e5e31bc55b9ed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee5342d9e6c4c18626b115552fa5ae243656d9865c0e80a73b7e9bfb4f8210ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userDomainNames")
    def user_domain_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userDomainNames"))

    @user_domain_names.setter
    def user_domain_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a5978cb9010818dea5257c2fe84ff52b10c5e8238f122c5d0760e4b131b2ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userDomainNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versioning")
    def versioning(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "versioning"))

    @versioning.setter
    def versioning(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c069e3205d73523881b2fba66c199808cb95e45a7cca38c11746f9751ec7ee0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versioning", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bucket": "bucket",
        "acl": "acl",
        "cors_rule": "corsRule",
        "event_notifications": "eventNotifications",
        "force_destroy": "forceDestroy",
        "id": "id",
        "lifecycle_rule": "lifecycleRule",
        "logging": "logging",
        "parallel_fs": "parallelFs",
        "region": "region",
        "server_side_encryption": "serverSideEncryption",
        "storage_class": "storageClass",
        "tags": "tags",
        "user_domain_names": "userDomainNames",
        "versioning": "versioning",
        "website": "website",
        "worm_policy": "wormPolicy",
    },
)
class ObsBucketConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bucket: builtins.str,
        acl: typing.Optional[builtins.str] = None,
        cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketCorsRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_notifications: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketEventNotifications", typing.Dict[builtins.str, typing.Any]]]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketLifecycleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        logging: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketLogging", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parallel_fs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        server_side_encryption: typing.Optional[typing.Union["ObsBucketServerSideEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_class: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        versioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        website: typing.Optional[typing.Union["ObsBucketWebsite", typing.Dict[builtins.str, typing.Any]]] = None,
        worm_policy: typing.Optional[typing.Union["ObsBucketWormPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#bucket ObsBucket#bucket}.
        :param acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#acl ObsBucket#acl}.
        :param cors_rule: cors_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#cors_rule ObsBucket#cors_rule}
        :param event_notifications: event_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#event_notifications ObsBucket#event_notifications}
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#force_destroy ObsBucket#force_destroy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#id ObsBucket#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lifecycle_rule: lifecycle_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#lifecycle_rule ObsBucket#lifecycle_rule}
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#logging ObsBucket#logging}
        :param parallel_fs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#parallel_fs ObsBucket#parallel_fs}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#region ObsBucket#region}.
        :param server_side_encryption: server_side_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#server_side_encryption ObsBucket#server_side_encryption}
        :param storage_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#storage_class ObsBucket#storage_class}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#tags ObsBucket#tags}.
        :param user_domain_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#user_domain_names ObsBucket#user_domain_names}.
        :param versioning: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#versioning ObsBucket#versioning}.
        :param website: website block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#website ObsBucket#website}
        :param worm_policy: worm_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#worm_policy ObsBucket#worm_policy}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(server_side_encryption, dict):
            server_side_encryption = ObsBucketServerSideEncryption(**server_side_encryption)
        if isinstance(website, dict):
            website = ObsBucketWebsite(**website)
        if isinstance(worm_policy, dict):
            worm_policy = ObsBucketWormPolicy(**worm_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718fc78934162aeee99f492664ac30ae4cc4d76d4553c8c814c8e5e660b5de48)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
            check_type(argname="argument cors_rule", value=cors_rule, expected_type=type_hints["cors_rule"])
            check_type(argname="argument event_notifications", value=event_notifications, expected_type=type_hints["event_notifications"])
            check_type(argname="argument force_destroy", value=force_destroy, expected_type=type_hints["force_destroy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lifecycle_rule", value=lifecycle_rule, expected_type=type_hints["lifecycle_rule"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument parallel_fs", value=parallel_fs, expected_type=type_hints["parallel_fs"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument server_side_encryption", value=server_side_encryption, expected_type=type_hints["server_side_encryption"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_domain_names", value=user_domain_names, expected_type=type_hints["user_domain_names"])
            check_type(argname="argument versioning", value=versioning, expected_type=type_hints["versioning"])
            check_type(argname="argument website", value=website, expected_type=type_hints["website"])
            check_type(argname="argument worm_policy", value=worm_policy, expected_type=type_hints["worm_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
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
        if acl is not None:
            self._values["acl"] = acl
        if cors_rule is not None:
            self._values["cors_rule"] = cors_rule
        if event_notifications is not None:
            self._values["event_notifications"] = event_notifications
        if force_destroy is not None:
            self._values["force_destroy"] = force_destroy
        if id is not None:
            self._values["id"] = id
        if lifecycle_rule is not None:
            self._values["lifecycle_rule"] = lifecycle_rule
        if logging is not None:
            self._values["logging"] = logging
        if parallel_fs is not None:
            self._values["parallel_fs"] = parallel_fs
        if region is not None:
            self._values["region"] = region
        if server_side_encryption is not None:
            self._values["server_side_encryption"] = server_side_encryption
        if storage_class is not None:
            self._values["storage_class"] = storage_class
        if tags is not None:
            self._values["tags"] = tags
        if user_domain_names is not None:
            self._values["user_domain_names"] = user_domain_names
        if versioning is not None:
            self._values["versioning"] = versioning
        if website is not None:
            self._values["website"] = website
        if worm_policy is not None:
            self._values["worm_policy"] = worm_policy

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
    def bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#bucket ObsBucket#bucket}.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def acl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#acl ObsBucket#acl}.'''
        result = self._values.get("acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketCorsRule"]]]:
        '''cors_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#cors_rule ObsBucket#cors_rule}
        '''
        result = self._values.get("cors_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketCorsRule"]]], result)

    @builtins.property
    def event_notifications(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketEventNotifications"]]]:
        '''event_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#event_notifications ObsBucket#event_notifications}
        '''
        result = self._values.get("event_notifications")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketEventNotifications"]]], result)

    @builtins.property
    def force_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#force_destroy ObsBucket#force_destroy}.'''
        result = self._values.get("force_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#id ObsBucket#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRule"]]]:
        '''lifecycle_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#lifecycle_rule ObsBucket#lifecycle_rule}
        '''
        result = self._values.get("lifecycle_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRule"]]], result)

    @builtins.property
    def logging(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLogging"]]]:
        '''logging block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#logging ObsBucket#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLogging"]]], result)

    @builtins.property
    def parallel_fs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#parallel_fs ObsBucket#parallel_fs}.'''
        result = self._values.get("parallel_fs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#region ObsBucket#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption(
        self,
    ) -> typing.Optional["ObsBucketServerSideEncryption"]:
        '''server_side_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#server_side_encryption ObsBucket#server_side_encryption}
        '''
        result = self._values.get("server_side_encryption")
        return typing.cast(typing.Optional["ObsBucketServerSideEncryption"], result)

    @builtins.property
    def storage_class(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#storage_class ObsBucket#storage_class}.'''
        result = self._values.get("storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#tags ObsBucket#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def user_domain_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#user_domain_names ObsBucket#user_domain_names}.'''
        result = self._values.get("user_domain_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def versioning(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#versioning ObsBucket#versioning}.'''
        result = self._values.get("versioning")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def website(self) -> typing.Optional["ObsBucketWebsite"]:
        '''website block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#website ObsBucket#website}
        '''
        result = self._values.get("website")
        return typing.cast(typing.Optional["ObsBucketWebsite"], result)

    @builtins.property
    def worm_policy(self) -> typing.Optional["ObsBucketWormPolicy"]:
        '''worm_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#worm_policy ObsBucket#worm_policy}
        '''
        result = self._values.get("worm_policy")
        return typing.cast(typing.Optional["ObsBucketWormPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketCorsRule",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_methods": "allowedMethods",
        "allowed_origins": "allowedOrigins",
        "allowed_headers": "allowedHeaders",
        "expose_headers": "exposeHeaders",
        "max_age_seconds": "maxAgeSeconds",
    },
)
class ObsBucketCorsRule:
    def __init__(
        self,
        *,
        allowed_methods: typing.Sequence[builtins.str],
        allowed_origins: typing.Sequence[builtins.str],
        allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_age_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allowed_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#allowed_methods ObsBucket#allowed_methods}.
        :param allowed_origins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#allowed_origins ObsBucket#allowed_origins}.
        :param allowed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#allowed_headers ObsBucket#allowed_headers}.
        :param expose_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#expose_headers ObsBucket#expose_headers}.
        :param max_age_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#max_age_seconds ObsBucket#max_age_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca795a644525e90c5301ef8484c152f48705a332f9b323d03d19ae56f93ab7b)
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
            check_type(argname="argument allowed_headers", value=allowed_headers, expected_type=type_hints["allowed_headers"])
            check_type(argname="argument expose_headers", value=expose_headers, expected_type=type_hints["expose_headers"])
            check_type(argname="argument max_age_seconds", value=max_age_seconds, expected_type=type_hints["max_age_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_methods": allowed_methods,
            "allowed_origins": allowed_origins,
        }
        if allowed_headers is not None:
            self._values["allowed_headers"] = allowed_headers
        if expose_headers is not None:
            self._values["expose_headers"] = expose_headers
        if max_age_seconds is not None:
            self._values["max_age_seconds"] = max_age_seconds

    @builtins.property
    def allowed_methods(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#allowed_methods ObsBucket#allowed_methods}.'''
        result = self._values.get("allowed_methods")
        assert result is not None, "Required property 'allowed_methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_origins(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#allowed_origins ObsBucket#allowed_origins}.'''
        result = self._values.get("allowed_origins")
        assert result is not None, "Required property 'allowed_origins' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#allowed_headers ObsBucket#allowed_headers}.'''
        result = self._values.get("allowed_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#expose_headers ObsBucket#expose_headers}.'''
        result = self._values.get("expose_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_age_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#max_age_seconds ObsBucket#max_age_seconds}.'''
        result = self._values.get("max_age_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketCorsRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketCorsRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketCorsRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3de78c68f8d431ecdbec7d04b34b7467043cd0a78261b0fa4c643927b72b0529)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ObsBucketCorsRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a624256081272a209cc29c34339b290fbc73e9fc5319f70d3dbd958cbbcbe48)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObsBucketCorsRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58be7c678af98dec69102d81a934c3eb587876ea71117fdf00ab8d5006d7d9d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__290b8bde3443c870368e88cc07ec5a4aaecd1319e261812ef3b6c8acb59085b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb41317a84e692feb958fd1fcf4a35af55edbf3969a9bdb6ffffc5657817c898)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketCorsRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketCorsRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketCorsRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eecd5098b17f1be96585e14603818771033c1de33b6df34651addff80a31ebd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObsBucketCorsRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketCorsRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99dc40ece255248e6df56cd804b7b556fb7675d4302f48f39a0d11f87f17a9ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedHeaders")
    def reset_allowed_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedHeaders", []))

    @jsii.member(jsii_name="resetExposeHeaders")
    def reset_expose_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExposeHeaders", []))

    @jsii.member(jsii_name="resetMaxAgeSeconds")
    def reset_max_age_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAgeSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="allowedHeadersInput")
    def allowed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedOriginsInput")
    def allowed_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="exposeHeadersInput")
    def expose_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exposeHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeSecondsInput")
    def max_age_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAgeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedHeaders")
    def allowed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedHeaders"))

    @allowed_headers.setter
    def allowed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__823e05bd24824c78e41c5c96c9b9198e4c7dab98438a1bdd1e599b68857f10f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMethods"))

    @allowed_methods.setter
    def allowed_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90a991affb6385a3692d158f671f976b6746fdbb9e6b6d0cdda519e047ea4c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOrigins"))

    @allowed_origins.setter
    def allowed_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03385a0b0c2ccacfd8f17a6557e6b569870eb0d7645cd5795964a2383e8d8e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOrigins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exposeHeaders")
    def expose_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exposeHeaders"))

    @expose_headers.setter
    def expose_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53baedb5fc12001d3babff86daa092175fce5973f2fa55f066ffc71a7c681c3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposeHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAgeSeconds")
    def max_age_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAgeSeconds"))

    @max_age_seconds.setter
    def max_age_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99bc060953e0f2374d33acb1fc8e0f57ee03fba6aa0160a35cb9aadae62bd06a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAgeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketCorsRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketCorsRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketCorsRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce0c5baa4449e150378504f77821350b5935a75d596c5cb4a2a07e2a24988e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketEventNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "events": "events",
        "topic": "topic",
        "filter_rule": "filterRule",
        "id": "id",
    },
)
class ObsBucketEventNotifications:
    def __init__(
        self,
        *,
        events: typing.Sequence[builtins.str],
        topic: builtins.str,
        filter_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketEventNotificationsFilterRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#events ObsBucket#events}.
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#topic ObsBucket#topic}.
        :param filter_rule: filter_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#filter_rule ObsBucket#filter_rule}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#id ObsBucket#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9aabf3e975f2fe7427a03fcc25c19443d62d403183caa5c360e0e511d35667)
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument filter_rule", value=filter_rule, expected_type=type_hints["filter_rule"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "events": events,
            "topic": topic,
        }
        if filter_rule is not None:
            self._values["filter_rule"] = filter_rule
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def events(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#events ObsBucket#events}.'''
        result = self._values.get("events")
        assert result is not None, "Required property 'events' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#topic ObsBucket#topic}.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketEventNotificationsFilterRule"]]]:
        '''filter_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#filter_rule ObsBucket#filter_rule}
        '''
        result = self._values.get("filter_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketEventNotificationsFilterRule"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#id ObsBucket#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketEventNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketEventNotificationsFilterRule",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ObsBucketEventNotificationsFilterRule:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#name ObsBucket#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#value ObsBucket#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea39ea2ac1e742899e255c8d72d8654a4082bcdcdf1b83d6689b92acd2249285)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#name ObsBucket#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#value ObsBucket#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketEventNotificationsFilterRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketEventNotificationsFilterRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketEventNotificationsFilterRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c68cbe19b30f27c5a4a16b32ee61e30245636660d2954d21f2c1e3a1bc31547)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObsBucketEventNotificationsFilterRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3865a745f2003275528e33c3e06b7958f294e7bbe19c4c420f236981ee1f002f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObsBucketEventNotificationsFilterRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3dcfbc61fef26447af7fbf6c49d2afd461b3aa2d6338b5ae9f857315ccb6aec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0b585f59fc457a53ef9a8ef7f67b86a4001cca235a337955f5415aae0da626a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55ef3ccb237e49bce3c6280f9740c2a2afffe1950ab4f56908b405964a6826a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketEventNotificationsFilterRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketEventNotificationsFilterRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketEventNotificationsFilterRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab234fd5c87d9712aa7f28c314104c828bd12c5bb5d02351f2359b3e5c1068ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObsBucketEventNotificationsFilterRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketEventNotificationsFilterRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f13fb5d173d0e60bf7e67e535864ffebbc51f66a9487e7618607055e3669268)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e4edd31356174d1c9ae8c65bc9ffe0ac5201eda13ba35c8d6af562fa4ff08be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48845bd6b65242b4d8bc3b0e7594c108bcd944b23d26a42c3dee591d3a0fa5ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketEventNotificationsFilterRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketEventNotificationsFilterRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketEventNotificationsFilterRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef96b45fa712eead14877ae302b170da8f15ca0afd47b3def0b80d894e325e25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObsBucketEventNotificationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketEventNotificationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b52cabc61481970bf813f23b1e92b9720312c3f5571c3bb4b12c7d178fd6a6a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ObsBucketEventNotificationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8720ca75c7e09c60d3562439429111d8865e12ac6f010c038042d2c1084eb4c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObsBucketEventNotificationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca367a8713aa49071e3629e781a416eb02843846c04165a15fdea9680941cd2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a3e4d3559a4e57044c29d7af12612f9945c84328c24fb8bd2dd197ddce33744)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8832c88b65b3cf36e305ead7242ac2704cbc3314d531568a813c0ad9c69616a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketEventNotifications]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketEventNotifications]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketEventNotifications]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd99440d3459eaee7d941645e8b05e200f5a771b1667387ff5f099a6edbfe3a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObsBucketEventNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketEventNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a0952c541475a369567f8365ee3f95cb5650c1faa431dec232e37fa190c393e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFilterRule")
    def put_filter_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketEventNotificationsFilterRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0082e9e4c5fd69febd94106f9baf6f33ad17ba3369cecb63dc722cff79c1d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilterRule", [value]))

    @jsii.member(jsii_name="resetFilterRule")
    def reset_filter_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterRule", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @builtins.property
    @jsii.member(jsii_name="filterRule")
    def filter_rule(self) -> ObsBucketEventNotificationsFilterRuleList:
        return typing.cast(ObsBucketEventNotificationsFilterRuleList, jsii.get(self, "filterRule"))

    @builtins.property
    @jsii.member(jsii_name="eventsInput")
    def events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eventsInput"))

    @builtins.property
    @jsii.member(jsii_name="filterRuleInput")
    def filter_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketEventNotificationsFilterRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketEventNotificationsFilterRule]]], jsii.get(self, "filterRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "events"))

    @events.setter
    def events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3577b019316a7b13556ab2395d34ee4959e079838264bac011f8711bb730ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "events", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9cb56498229f72e9acbd40d1eb0a9dd35c122eaebb5dc6c6ffdff3d8e4126da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__168c6ab0531d8208524cb3b69b4625c1a95e83b62a8f9b57528b57e85a053462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketEventNotifications]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketEventNotifications]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketEventNotifications]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f5b4c7a9c08b5810e7045cccf588a40a0861d2d4dabb03fdb86e1f9e927b0d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRule",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "name": "name",
        "expiration": "expiration",
        "noncurrent_version_expiration": "noncurrentVersionExpiration",
        "noncurrent_version_transition": "noncurrentVersionTransition",
        "prefix": "prefix",
        "tag": "tag",
        "transition": "transition",
    },
)
class ObsBucketLifecycleRule:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        expiration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketLifecycleRuleExpiration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        noncurrent_version_expiration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketLifecycleRuleNoncurrentVersionExpiration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        noncurrent_version_transition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketLifecycleRuleNoncurrentVersionTransition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        prefix: typing.Optional[builtins.str] = None,
        tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketLifecycleRuleTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
        transition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketLifecycleRuleTransition", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#enabled ObsBucket#enabled}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#name ObsBucket#name}.
        :param expiration: expiration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#expiration ObsBucket#expiration}
        :param noncurrent_version_expiration: noncurrent_version_expiration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#noncurrent_version_expiration ObsBucket#noncurrent_version_expiration}
        :param noncurrent_version_transition: noncurrent_version_transition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#noncurrent_version_transition ObsBucket#noncurrent_version_transition}
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#prefix ObsBucket#prefix}.
        :param tag: tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#tag ObsBucket#tag}
        :param transition: transition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#transition ObsBucket#transition}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8262dd0f5a66cd41547015826014331a7cd0ef68ee54036f9ca6c16820f66d80)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument expiration", value=expiration, expected_type=type_hints["expiration"])
            check_type(argname="argument noncurrent_version_expiration", value=noncurrent_version_expiration, expected_type=type_hints["noncurrent_version_expiration"])
            check_type(argname="argument noncurrent_version_transition", value=noncurrent_version_transition, expected_type=type_hints["noncurrent_version_transition"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument transition", value=transition, expected_type=type_hints["transition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "name": name,
        }
        if expiration is not None:
            self._values["expiration"] = expiration
        if noncurrent_version_expiration is not None:
            self._values["noncurrent_version_expiration"] = noncurrent_version_expiration
        if noncurrent_version_transition is not None:
            self._values["noncurrent_version_transition"] = noncurrent_version_transition
        if prefix is not None:
            self._values["prefix"] = prefix
        if tag is not None:
            self._values["tag"] = tag
        if transition is not None:
            self._values["transition"] = transition

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#enabled ObsBucket#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#name ObsBucket#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRuleExpiration"]]]:
        '''expiration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#expiration ObsBucket#expiration}
        '''
        result = self._values.get("expiration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRuleExpiration"]]], result)

    @builtins.property
    def noncurrent_version_expiration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRuleNoncurrentVersionExpiration"]]]:
        '''noncurrent_version_expiration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#noncurrent_version_expiration ObsBucket#noncurrent_version_expiration}
        '''
        result = self._values.get("noncurrent_version_expiration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRuleNoncurrentVersionExpiration"]]], result)

    @builtins.property
    def noncurrent_version_transition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRuleNoncurrentVersionTransition"]]]:
        '''noncurrent_version_transition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#noncurrent_version_transition ObsBucket#noncurrent_version_transition}
        '''
        result = self._values.get("noncurrent_version_transition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRuleNoncurrentVersionTransition"]]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#prefix ObsBucket#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRuleTag"]]]:
        '''tag block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#tag ObsBucket#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRuleTag"]]], result)

    @builtins.property
    def transition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRuleTransition"]]]:
        '''transition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#transition ObsBucket#transition}
        '''
        result = self._values.get("transition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRuleTransition"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketLifecycleRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleExpiration",
    jsii_struct_bases=[],
    name_mapping={"days": "days"},
)
class ObsBucketLifecycleRuleExpiration:
    def __init__(self, *, days: jsii.Number) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#days ObsBucket#days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58bf4258df8ac0f4478a72398e0e7e3264298d559b01bc1d6ded1eb6d950f792)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "days": days,
        }

    @builtins.property
    def days(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#days ObsBucket#days}.'''
        result = self._values.get("days")
        assert result is not None, "Required property 'days' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketLifecycleRuleExpiration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketLifecycleRuleExpirationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleExpirationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb23e1190f5e555ace9580987ea0995944429cc5fb21323b421de9661b6c95f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObsBucketLifecycleRuleExpirationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e12aa5f33c8297ee265da6a50e43a6259bc37150fe74a56ed18c971585a25c14)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObsBucketLifecycleRuleExpirationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8df5b12fe3409e76c550db4c81cf449d138b1cc02fae7eb8549c20f364150d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc51cbb1caaa1ea334c96abc43dc057d4280300a6587ae0dd82b742d0a61c23a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8a7b64a80d934ee54c658ae18363d2b9a91c0393aeb0348e86997a40545c4b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleExpiration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleExpiration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleExpiration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__273d0b1e249571e838bcdae4a887f038223634cdd49085a01d057eae33fcb9bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObsBucketLifecycleRuleExpirationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleExpirationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9715ec01f7a7d653554aaf5441795b3f80228e8134f84072c803ba910bdc685)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "days"))

    @days.setter
    def days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1475fdea07552f08acd2cf1842a054b8fc67b9561441c4d1c5093e50a9792bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleExpiration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleExpiration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleExpiration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee2a1fe6414d51359d73b3adb11d052626f121d2ba29a1c4645c7ad03401d78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObsBucketLifecycleRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6bec10ad7bcad9323907034b9e63d79340386d443872b492405cd82569c271b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ObsBucketLifecycleRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d77494ee9860ae487611f8cd8fc355ece6e745334585a297ef54522dd9b933c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObsBucketLifecycleRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b9269cd1f99e17913cd2f7c73fbdfd5b889e7a296cc7db89b339cf18ef4569)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62d5fb464e14fb92a59f4e058e3d00c1d78e70fade6e6f67f7797239d2804d04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fda4ce7b85af80fcd922dc558db1614c340361fba0916b74a3322b4af1433877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f9b23e26e7318e2373f1a7aa133da299b7b030218059f8e1450796edd8e5ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleNoncurrentVersionExpiration",
    jsii_struct_bases=[],
    name_mapping={"days": "days"},
)
class ObsBucketLifecycleRuleNoncurrentVersionExpiration:
    def __init__(self, *, days: jsii.Number) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#days ObsBucket#days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1eda33096896a94096508745a24cc184829498ba827d53f048c03e0c717c19b)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "days": days,
        }

    @builtins.property
    def days(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#days ObsBucket#days}.'''
        result = self._values.get("days")
        assert result is not None, "Required property 'days' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketLifecycleRuleNoncurrentVersionExpiration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketLifecycleRuleNoncurrentVersionExpirationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleNoncurrentVersionExpirationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69936f29c840a9cab9056e4684f72b6d0f53b1049f24b5ea3585b3e04261915d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObsBucketLifecycleRuleNoncurrentVersionExpirationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__409d96276b46ca31aca8f62d4b466ed46c2bc935d1cf09f51aa443675d2ca758)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObsBucketLifecycleRuleNoncurrentVersionExpirationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac1205a1e4ab77551335b6fe1be464124da616e63185a15ad7e754a64e01e770)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5540fe3a5af8e5c02b10964fc1f2925c846355fe90c6bdf49c634208ddf14151)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f2a8377355a727dff84b5e04ba7804d4654b659c07438753d7862be7071eb53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleNoncurrentVersionExpiration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleNoncurrentVersionExpiration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleNoncurrentVersionExpiration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa5b083507f745b9b95a665b97de6067a355b922fb9f9a6e8cfe6e1d21f54185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObsBucketLifecycleRuleNoncurrentVersionExpirationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleNoncurrentVersionExpirationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b92f18d2b5590f69f7e2942ee21495e7155459cf03217a1e1da7dcfa14c59db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "days"))

    @days.setter
    def days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f9452bc9bb9e3ca955df69346638cc36a93a9dcfcb54302d74939121e10a399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleNoncurrentVersionExpiration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleNoncurrentVersionExpiration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleNoncurrentVersionExpiration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b7d0b3f9b6947881d70547c62e441d29c64bf796cd498ef56e9b78c569c7c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleNoncurrentVersionTransition",
    jsii_struct_bases=[],
    name_mapping={"days": "days", "storage_class": "storageClass"},
)
class ObsBucketLifecycleRuleNoncurrentVersionTransition:
    def __init__(self, *, days: jsii.Number, storage_class: builtins.str) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#days ObsBucket#days}.
        :param storage_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#storage_class ObsBucket#storage_class}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b8e36cd52dec4814c4ac4e7b53539e42fdb0094aa871cc076c34649f96d8a4)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "days": days,
            "storage_class": storage_class,
        }

    @builtins.property
    def days(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#days ObsBucket#days}.'''
        result = self._values.get("days")
        assert result is not None, "Required property 'days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def storage_class(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#storage_class ObsBucket#storage_class}.'''
        result = self._values.get("storage_class")
        assert result is not None, "Required property 'storage_class' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketLifecycleRuleNoncurrentVersionTransition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketLifecycleRuleNoncurrentVersionTransitionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleNoncurrentVersionTransitionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b5095c91b45f583396758887c7c0db2e0d2c8522675f032838b2ac41a5e6cfb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObsBucketLifecycleRuleNoncurrentVersionTransitionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a34d4f82f83bc2de6d2c71c24f91ad30424da5cfb3dccd7e99c32c647b9a5ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObsBucketLifecycleRuleNoncurrentVersionTransitionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5787356d31d6081c04b247f4d01e9af01d6977d172cd68e1362c630fe1a438a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__162a3db165c2eab8d88dee179936b34d3699b0cca8c774ad4c08276fcd310a36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dce15b2bc3be75ab97bc544dff4212419de724ba1ef68bd7b5feadf762ee587)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleNoncurrentVersionTransition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleNoncurrentVersionTransition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleNoncurrentVersionTransition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035e456c37f291318d7827f7b67573cd61b170a6f7620a9f81cc9a3309866ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObsBucketLifecycleRuleNoncurrentVersionTransitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleNoncurrentVersionTransitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31bf2370b118ce2c681444bf899362cdc87a582c9f33771d15a236854947a308)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="storageClassInput")
    def storage_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "days"))

    @days.setter
    def days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b5fc48af38eac1189e920a5761ab05e90401d41bdc27722362ad337926b4d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf3bb7415464585cc5ac122616c9c3e2602c6b483e67b9dfad414d5e885bcef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleNoncurrentVersionTransition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleNoncurrentVersionTransition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleNoncurrentVersionTransition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a6b1aff9adce31eb8bb72936c899b6ee243697400329aff0429dc6d926d057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObsBucketLifecycleRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb01c8682a6b1b26be8ec2c0283ca16e2f3500f689d870a234e0b59e0c8e7a71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExpiration")
    def put_expiration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRuleExpiration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3821ce83584c937b53f0bcc62ef93eb25452053bb7543163f9550f4881357051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExpiration", [value]))

    @jsii.member(jsii_name="putNoncurrentVersionExpiration")
    def put_noncurrent_version_expiration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRuleNoncurrentVersionExpiration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d488f012a2119ee80659bf3c9003b0aac3fd92904a22e4836ebfb5e70c3b3435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNoncurrentVersionExpiration", [value]))

    @jsii.member(jsii_name="putNoncurrentVersionTransition")
    def put_noncurrent_version_transition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRuleNoncurrentVersionTransition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ae681cc8dc47163f037d73c0f97176e4b88e81912979cf46bfaf653a2ec417a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNoncurrentVersionTransition", [value]))

    @jsii.member(jsii_name="putTag")
    def put_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketLifecycleRuleTag", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7444f67b894ba2eef11f6ff0c91b0a6e4c06035fe49547e928423f97f52dc250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTag", [value]))

    @jsii.member(jsii_name="putTransition")
    def put_transition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketLifecycleRuleTransition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da7222f2d07b4b1a44f74ec98c71020fb94c907afb273dfdeb93be4938b1a79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTransition", [value]))

    @jsii.member(jsii_name="resetExpiration")
    def reset_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiration", []))

    @jsii.member(jsii_name="resetNoncurrentVersionExpiration")
    def reset_noncurrent_version_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoncurrentVersionExpiration", []))

    @jsii.member(jsii_name="resetNoncurrentVersionTransition")
    def reset_noncurrent_version_transition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoncurrentVersionTransition", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="resetTransition")
    def reset_transition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransition", []))

    @builtins.property
    @jsii.member(jsii_name="expiration")
    def expiration(self) -> ObsBucketLifecycleRuleExpirationList:
        return typing.cast(ObsBucketLifecycleRuleExpirationList, jsii.get(self, "expiration"))

    @builtins.property
    @jsii.member(jsii_name="noncurrentVersionExpiration")
    def noncurrent_version_expiration(
        self,
    ) -> ObsBucketLifecycleRuleNoncurrentVersionExpirationList:
        return typing.cast(ObsBucketLifecycleRuleNoncurrentVersionExpirationList, jsii.get(self, "noncurrentVersionExpiration"))

    @builtins.property
    @jsii.member(jsii_name="noncurrentVersionTransition")
    def noncurrent_version_transition(
        self,
    ) -> ObsBucketLifecycleRuleNoncurrentVersionTransitionList:
        return typing.cast(ObsBucketLifecycleRuleNoncurrentVersionTransitionList, jsii.get(self, "noncurrentVersionTransition"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> "ObsBucketLifecycleRuleTagList":
        return typing.cast("ObsBucketLifecycleRuleTagList", jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="transition")
    def transition(self) -> "ObsBucketLifecycleRuleTransitionList":
        return typing.cast("ObsBucketLifecycleRuleTransitionList", jsii.get(self, "transition"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationInput")
    def expiration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleExpiration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleExpiration]]], jsii.get(self, "expirationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="noncurrentVersionExpirationInput")
    def noncurrent_version_expiration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleNoncurrentVersionExpiration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleNoncurrentVersionExpiration]]], jsii.get(self, "noncurrentVersionExpirationInput"))

    @builtins.property
    @jsii.member(jsii_name="noncurrentVersionTransitionInput")
    def noncurrent_version_transition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleNoncurrentVersionTransition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleNoncurrentVersionTransition]]], jsii.get(self, "noncurrentVersionTransitionInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRuleTag"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRuleTag"]]], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="transitionInput")
    def transition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRuleTransition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketLifecycleRuleTransition"]]], jsii.get(self, "transitionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b09f29d370accb544f5f624d379c367e3e6ecccca42f6e598b24fe1fcca26a27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d236b1dd86b8ac76c9df9400bb477292abe728a8f8beda60ba2d7c1de9b8698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__507f73ad48072859b5658a75bf9b5d365455108aedd2887392dd5445773e67cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91985d23d0383731fe8fd7261c1a8537ab7347343d927ad3baf586e8d4d169b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleTag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class ObsBucketLifecycleRuleTag:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#key ObsBucket#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#value ObsBucket#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e868f1d4924a9c10b1900c2caa4c36fa9f89733be43c49f3858cda220fa2e7)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#key ObsBucket#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#value ObsBucket#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketLifecycleRuleTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketLifecycleRuleTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a254c64fb181cfe89a7dab21134260f7f4803c16d015bb91ddfc130903070d2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ObsBucketLifecycleRuleTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f95e9966d3de5b8a8e617c23c2dbd780a0b856a5edd98887486dd91e8afcbfb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObsBucketLifecycleRuleTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49f329f134922fe2ba344bba7c33a77bd980817abfad89f44dd472727cdb3ccf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2097e1855d6361f063331cda55ec8e58ab2126f32d09e2f43c41feb2a554ce5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8aea73bf00d09d9f49c508423dab2dea6400e1b5872c3e3908e365f2d9114be3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de00c98898893be017f20eb219a9713cd0831b69582317614b904ddb78a22b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObsBucketLifecycleRuleTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52692a9a261b87283af580f1ef59f931d72b247e60c3c18efe71a21f56192b2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d1c1ef8cbec76827c7e9dd2325758afe269da7dd5da7afc994a6c94687f8ab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__769e882b74e7d51a9bb69fbc1505f06ce46712d28b19fb00213c94a645d2d093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleTag]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleTag]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleTag]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9821cae8cbe7689b028917950687bc5f362ea7b827569c3e6dd8078f0daf29c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleTransition",
    jsii_struct_bases=[],
    name_mapping={"days": "days", "storage_class": "storageClass"},
)
class ObsBucketLifecycleRuleTransition:
    def __init__(self, *, days: jsii.Number, storage_class: builtins.str) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#days ObsBucket#days}.
        :param storage_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#storage_class ObsBucket#storage_class}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f5b1de372798966fb45a252f57991d3912b4cf0290752ddfeaba86b7bc29b26)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "days": days,
            "storage_class": storage_class,
        }

    @builtins.property
    def days(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#days ObsBucket#days}.'''
        result = self._values.get("days")
        assert result is not None, "Required property 'days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def storage_class(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#storage_class ObsBucket#storage_class}.'''
        result = self._values.get("storage_class")
        assert result is not None, "Required property 'storage_class' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketLifecycleRuleTransition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketLifecycleRuleTransitionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleTransitionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58e255df9388734dd459d0cb91752836d412d71b35435bbf59e32794e119f59b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObsBucketLifecycleRuleTransitionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__521d15c46e7bf40a8635332233768eabbfb28f16e1a417db6696256b4b6b03d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObsBucketLifecycleRuleTransitionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f8845b564b24de6e151d9ba001202fc125c179ae28423c2729cdd0bb09136f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81a09b9d90b6d164614790002c49cbab171516a772f9bce33479c1f7ee1d0801)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82012b85ed196a3a717106a6db67a343c99473ed30203bdbb561ae7107e9602a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleTransition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleTransition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleTransition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c68271d2a0ac7be8de115b29c89bde897fe9cf479ac07015f569d8e833248a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObsBucketLifecycleRuleTransitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLifecycleRuleTransitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b7ca479111409ae0374c672abf852e2e9fe7447433b14f794980471709e5809)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="storageClassInput")
    def storage_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "days"))

    @days.setter
    def days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d086b997092af36749d7c9e05688c59f035481ccd9217ea864be26dc118d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11eb374e8a09784c87682327cc99f847803215dcb74e58ef01e950e5e99b9a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleTransition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleTransition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleTransition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e68df23c9de3258660350ad47bdab31530d4ee82a357110f87f47283f83c392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLogging",
    jsii_struct_bases=[],
    name_mapping={
        "target_bucket": "targetBucket",
        "agency": "agency",
        "target_prefix": "targetPrefix",
    },
)
class ObsBucketLogging:
    def __init__(
        self,
        *,
        target_bucket: builtins.str,
        agency: typing.Optional[builtins.str] = None,
        target_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#target_bucket ObsBucket#target_bucket}.
        :param agency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#agency ObsBucket#agency}.
        :param target_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#target_prefix ObsBucket#target_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faefe30996e057d765d999dc4493309b3d73685bcffb404e659182a483d2161b)
            check_type(argname="argument target_bucket", value=target_bucket, expected_type=type_hints["target_bucket"])
            check_type(argname="argument agency", value=agency, expected_type=type_hints["agency"])
            check_type(argname="argument target_prefix", value=target_prefix, expected_type=type_hints["target_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_bucket": target_bucket,
        }
        if agency is not None:
            self._values["agency"] = agency
        if target_prefix is not None:
            self._values["target_prefix"] = target_prefix

    @builtins.property
    def target_bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#target_bucket ObsBucket#target_bucket}.'''
        result = self._values.get("target_bucket")
        assert result is not None, "Required property 'target_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agency(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#agency ObsBucket#agency}.'''
        result = self._values.get("agency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#target_prefix ObsBucket#target_prefix}.'''
        result = self._values.get("target_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketLogging(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketLoggingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLoggingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a082966d7be9102005f602d0aca5ad344082022481c4b5cae3d98685516f8b14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ObsBucketLoggingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80884a2936f7a3fedd951d4706db4acf4b010273504d67869467c215bbc2ee27)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObsBucketLoggingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c195416c491c30915ec07c3e6624de32b5e6332ea50244b0993bdc7d93d77c16)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b87aa9b40f74cda545380d48382d6551731931a7bd48d4af02651301411dbbad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79a7c01c614a23f4d0755180449bbc25200257245e5162150d44ac631a2be0f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLogging]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLogging]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLogging]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59facc45e2b68bb5caa517e4c3c5506d1f45ef6eec8b1b13fda828fda925a6fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObsBucketLoggingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketLoggingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9b612f4d8498b47d9ae1405a7fe854df83a4617fc6ceecc74ce69cbb3d9efac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAgency")
    def reset_agency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgency", []))

    @jsii.member(jsii_name="resetTargetPrefix")
    def reset_target_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="agencyInput")
    def agency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyInput"))

    @builtins.property
    @jsii.member(jsii_name="targetBucketInput")
    def target_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="targetPrefixInput")
    def target_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="agency")
    def agency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agency"))

    @agency.setter
    def agency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4c1a086f7525e97cc4c7344f99c2c90599a25bd991cc75e405623832b1c1e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetBucket")
    def target_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetBucket"))

    @target_bucket.setter
    def target_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a9e4252838b0296d23cb2d2a1aacb5b1b3c12749d1099d21c15870301540942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPrefix")
    def target_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetPrefix"))

    @target_prefix.setter
    def target_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d645937f30ae74e3489e2c173ea16ea006f718c5cbbf9bac92972c1e4258f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLogging]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLogging]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLogging]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd26a88df1b5c68c11d9e7ed7292003e8d848f1411e230b953db2d72d6a2a5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketServerSideEncryption",
    jsii_struct_bases=[],
    name_mapping={
        "algorithm": "algorithm",
        "kms_key_id": "kmsKeyId",
        "kms_project_id": "kmsProjectId",
    },
)
class ObsBucketServerSideEncryption:
    def __init__(
        self,
        *,
        algorithm: builtins.str,
        kms_key_id: builtins.str,
        kms_project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#algorithm ObsBucket#algorithm}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#kms_key_id ObsBucket#kms_key_id}.
        :param kms_project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#kms_project_id ObsBucket#kms_project_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4322da4776a5cd1352d6de284f41d3eaca3cae093f6a5b5ab7f4bd12978d39)
            check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument kms_project_id", value=kms_project_id, expected_type=type_hints["kms_project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "algorithm": algorithm,
            "kms_key_id": kms_key_id,
        }
        if kms_project_id is not None:
            self._values["kms_project_id"] = kms_project_id

    @builtins.property
    def algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#algorithm ObsBucket#algorithm}.'''
        result = self._values.get("algorithm")
        assert result is not None, "Required property 'algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#kms_key_id ObsBucket#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        assert result is not None, "Required property 'kms_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_project_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#kms_project_id ObsBucket#kms_project_id}.'''
        result = self._values.get("kms_project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketServerSideEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketServerSideEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketServerSideEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ae2e8b52d243da387c95129d0487855a15826475bb098ee0d820f45d263a4d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsProjectId")
    def reset_kms_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsProjectId", []))

    @builtins.property
    @jsii.member(jsii_name="algorithmInput")
    def algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "algorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsProjectIdInput")
    def kms_project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "algorithm"))

    @algorithm.setter
    def algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0331f7186898b1b60b7d48b1c6f9d7d11346cbfe66d6ee204bda151504b93bae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "algorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48120a022abbf9082a90b03c76e43b85210e14a81ec6ddafc6ade6ddc6dc6952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsProjectId")
    def kms_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsProjectId"))

    @kms_project_id.setter
    def kms_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf1ada751e585142fdcc2007a04a1b7ef373e1d1c59a6ffdca24b93d9cebe051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ObsBucketServerSideEncryption]:
        return typing.cast(typing.Optional[ObsBucketServerSideEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ObsBucketServerSideEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d54b0ce04d544f4e5738886efadabffd5c78bc27981c569ae41f1121b59a3a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketWebsite",
    jsii_struct_bases=[],
    name_mapping={
        "error_document": "errorDocument",
        "index_document": "indexDocument",
        "redirect_all_requests_to": "redirectAllRequestsTo",
        "routing_rules": "routingRules",
    },
)
class ObsBucketWebsite:
    def __init__(
        self,
        *,
        error_document: typing.Optional[builtins.str] = None,
        index_document: typing.Optional[builtins.str] = None,
        redirect_all_requests_to: typing.Optional[builtins.str] = None,
        routing_rules: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param error_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#error_document ObsBucket#error_document}.
        :param index_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#index_document ObsBucket#index_document}.
        :param redirect_all_requests_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#redirect_all_requests_to ObsBucket#redirect_all_requests_to}.
        :param routing_rules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#routing_rules ObsBucket#routing_rules}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f2be9a2a5d3c664a9a1387dd6faf477b0f6af039b239e9f498be43005f9f62)
            check_type(argname="argument error_document", value=error_document, expected_type=type_hints["error_document"])
            check_type(argname="argument index_document", value=index_document, expected_type=type_hints["index_document"])
            check_type(argname="argument redirect_all_requests_to", value=redirect_all_requests_to, expected_type=type_hints["redirect_all_requests_to"])
            check_type(argname="argument routing_rules", value=routing_rules, expected_type=type_hints["routing_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if error_document is not None:
            self._values["error_document"] = error_document
        if index_document is not None:
            self._values["index_document"] = index_document
        if redirect_all_requests_to is not None:
            self._values["redirect_all_requests_to"] = redirect_all_requests_to
        if routing_rules is not None:
            self._values["routing_rules"] = routing_rules

    @builtins.property
    def error_document(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#error_document ObsBucket#error_document}.'''
        result = self._values.get("error_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index_document(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#index_document ObsBucket#index_document}.'''
        result = self._values.get("index_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_all_requests_to(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#redirect_all_requests_to ObsBucket#redirect_all_requests_to}.'''
        result = self._values.get("redirect_all_requests_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_rules(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#routing_rules ObsBucket#routing_rules}.'''
        result = self._values.get("routing_rules")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketWebsite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketWebsiteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketWebsiteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a58a526cf7f5181ce525232ed42f04cf130da6834aab329d0b40851b41bca84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetErrorDocument")
    def reset_error_document(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorDocument", []))

    @jsii.member(jsii_name="resetIndexDocument")
    def reset_index_document(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndexDocument", []))

    @jsii.member(jsii_name="resetRedirectAllRequestsTo")
    def reset_redirect_all_requests_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectAllRequestsTo", []))

    @jsii.member(jsii_name="resetRoutingRules")
    def reset_routing_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingRules", []))

    @builtins.property
    @jsii.member(jsii_name="errorDocumentInput")
    def error_document_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "errorDocumentInput"))

    @builtins.property
    @jsii.member(jsii_name="indexDocumentInput")
    def index_document_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexDocumentInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectAllRequestsToInput")
    def redirect_all_requests_to_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectAllRequestsToInput"))

    @builtins.property
    @jsii.member(jsii_name="routingRulesInput")
    def routing_rules_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="errorDocument")
    def error_document(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorDocument"))

    @error_document.setter
    def error_document(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4983755d470b097d7d8789f024e13103b0a81df0ccf7974b9b1dbdfeb7691036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorDocument", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indexDocument")
    def index_document(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexDocument"))

    @index_document.setter
    def index_document(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718f02598255b21e8b6b2114256e49c1095040ba62a86f45bf636bb8394d80df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexDocument", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectAllRequestsTo")
    def redirect_all_requests_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectAllRequestsTo"))

    @redirect_all_requests_to.setter
    def redirect_all_requests_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2164a93af8ea029694fa502ca9070ca44f3ef42e935991808b261d050373bf42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectAllRequestsTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingRules")
    def routing_rules(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingRules"))

    @routing_rules.setter
    def routing_rules(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8167ece7de8d6fda514e25081932228576955d237f55130036285cc870444d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ObsBucketWebsite]:
        return typing.cast(typing.Optional[ObsBucketWebsite], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ObsBucketWebsite]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0be37506e49ca39f6bc87d92b29c66f9df836ff7322b432b63867eb7d26e5709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketWormPolicy",
    jsii_struct_bases=[],
    name_mapping={"days": "days", "years": "years"},
)
class ObsBucketWormPolicy:
    def __init__(
        self,
        *,
        days: typing.Optional[jsii.Number] = None,
        years: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#days ObsBucket#days}.
        :param years: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#years ObsBucket#years}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063731e4b5f1c7078cb9399e808475e3bf068d0867e38b4e42d42cb281b97f6d)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            check_type(argname="argument years", value=years, expected_type=type_hints["years"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if days is not None:
            self._values["days"] = days
        if years is not None:
            self._values["years"] = years

    @builtins.property
    def days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#days ObsBucket#days}.'''
        result = self._values.get("days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def years(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket#years ObsBucket#years}.'''
        result = self._values.get("years")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketWormPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketWormPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucket.ObsBucketWormPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59f1cc00240e2d13466ca484bf9fbbdde4405927408f1adcbe1b00c209b6457a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDays")
    def reset_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDays", []))

    @jsii.member(jsii_name="resetYears")
    def reset_years(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYears", []))

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="yearsInput")
    def years_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearsInput"))

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "days"))

    @days.setter
    def days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b9f1bbdc509502add69dd55b0bac071b57b6552f5ad324ec81ec1b71f0c5047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="years")
    def years(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "years"))

    @years.setter
    def years(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdcbf0a9cc23aaab7b2be21622acfd79f522d551db17cdbd1ce817be25bdc522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "years", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ObsBucketWormPolicy]:
        return typing.cast(typing.Optional[ObsBucketWormPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ObsBucketWormPolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc25460aa918dd26e4a9c1e76b383467588ab7b12e55b957cc45c822133b68ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ObsBucket",
    "ObsBucketConfig",
    "ObsBucketCorsRule",
    "ObsBucketCorsRuleList",
    "ObsBucketCorsRuleOutputReference",
    "ObsBucketEventNotifications",
    "ObsBucketEventNotificationsFilterRule",
    "ObsBucketEventNotificationsFilterRuleList",
    "ObsBucketEventNotificationsFilterRuleOutputReference",
    "ObsBucketEventNotificationsList",
    "ObsBucketEventNotificationsOutputReference",
    "ObsBucketLifecycleRule",
    "ObsBucketLifecycleRuleExpiration",
    "ObsBucketLifecycleRuleExpirationList",
    "ObsBucketLifecycleRuleExpirationOutputReference",
    "ObsBucketLifecycleRuleList",
    "ObsBucketLifecycleRuleNoncurrentVersionExpiration",
    "ObsBucketLifecycleRuleNoncurrentVersionExpirationList",
    "ObsBucketLifecycleRuleNoncurrentVersionExpirationOutputReference",
    "ObsBucketLifecycleRuleNoncurrentVersionTransition",
    "ObsBucketLifecycleRuleNoncurrentVersionTransitionList",
    "ObsBucketLifecycleRuleNoncurrentVersionTransitionOutputReference",
    "ObsBucketLifecycleRuleOutputReference",
    "ObsBucketLifecycleRuleTag",
    "ObsBucketLifecycleRuleTagList",
    "ObsBucketLifecycleRuleTagOutputReference",
    "ObsBucketLifecycleRuleTransition",
    "ObsBucketLifecycleRuleTransitionList",
    "ObsBucketLifecycleRuleTransitionOutputReference",
    "ObsBucketLogging",
    "ObsBucketLoggingList",
    "ObsBucketLoggingOutputReference",
    "ObsBucketServerSideEncryption",
    "ObsBucketServerSideEncryptionOutputReference",
    "ObsBucketWebsite",
    "ObsBucketWebsiteOutputReference",
    "ObsBucketWormPolicy",
    "ObsBucketWormPolicyOutputReference",
]

publication.publish()

def _typecheckingstub__4d6614c59b8ea0d96dad0c1d6dde0756436ef254a4d38d5c41df70b47d070c71(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bucket: builtins.str,
    acl: typing.Optional[builtins.str] = None,
    cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketCorsRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_notifications: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketEventNotifications, typing.Dict[builtins.str, typing.Any]]]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    logging: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLogging, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parallel_fs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    server_side_encryption: typing.Optional[typing.Union[ObsBucketServerSideEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_class: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    user_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    versioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    website: typing.Optional[typing.Union[ObsBucketWebsite, typing.Dict[builtins.str, typing.Any]]] = None,
    worm_policy: typing.Optional[typing.Union[ObsBucketWormPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__73336310d79043ca4eee1cf681341c7abba4a8b78ecd4e37a1cde9630e892251(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd750a90c7aead9e48f2e0304af03b6fc8326e66779020b0edb81b1c693675e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketCorsRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e3e91a76189732f19bc9467cdf14cd21cc8eff84ca5d5376426d0766320292(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketEventNotifications, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1980a1c652b8a3c196fde5215b949c9c357b8e4160a766c9be8f595517636748(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f90561b1d322b870d758571ec56cf1b4f4758a1344f21c7c6a5693f39c2549f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLogging, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d9404cbf6d9954421f230f4526740eca919037f90531b2bda4f25bc2f01fbdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12aecb0bba794527e0211533fc9c9a5cec8c1a084ea3e7ca82ca4720d079cfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b470f43269c293cd8b342666d66badc8c4ba5210ba6001b7f7261701fed78516(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ea99a6dd45c5c3a3991c9fa3327deeeb3acfd0ce799034a89fbfca98137fb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2913dfeac99d6b28d5f87deb2012b9131ed2ad8601fb243611898a76a5fdbf50(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff96e25e196e1d8211303075e6b9134eccd7812257def1bc26e15348f8280ed4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af52c3e2cd190e1de26ac1c0fd1f7eeef284268f187773e71e5e31bc55b9ed9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5342d9e6c4c18626b115552fa5ae243656d9865c0e80a73b7e9bfb4f8210ab(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a5978cb9010818dea5257c2fe84ff52b10c5e8238f122c5d0760e4b131b2ce(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c069e3205d73523881b2fba66c199808cb95e45a7cca38c11746f9751ec7ee0d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718fc78934162aeee99f492664ac30ae4cc4d76d4553c8c814c8e5e660b5de48(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bucket: builtins.str,
    acl: typing.Optional[builtins.str] = None,
    cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketCorsRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_notifications: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketEventNotifications, typing.Dict[builtins.str, typing.Any]]]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    logging: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLogging, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parallel_fs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    server_side_encryption: typing.Optional[typing.Union[ObsBucketServerSideEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_class: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    user_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    versioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    website: typing.Optional[typing.Union[ObsBucketWebsite, typing.Dict[builtins.str, typing.Any]]] = None,
    worm_policy: typing.Optional[typing.Union[ObsBucketWormPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca795a644525e90c5301ef8484c152f48705a332f9b323d03d19ae56f93ab7b(
    *,
    allowed_methods: typing.Sequence[builtins.str],
    allowed_origins: typing.Sequence[builtins.str],
    allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_age_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de78c68f8d431ecdbec7d04b34b7467043cd0a78261b0fa4c643927b72b0529(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a624256081272a209cc29c34339b290fbc73e9fc5319f70d3dbd958cbbcbe48(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58be7c678af98dec69102d81a934c3eb587876ea71117fdf00ab8d5006d7d9d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290b8bde3443c870368e88cc07ec5a4aaecd1319e261812ef3b6c8acb59085b9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb41317a84e692feb958fd1fcf4a35af55edbf3969a9bdb6ffffc5657817c898(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eecd5098b17f1be96585e14603818771033c1de33b6df34651addff80a31ebd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketCorsRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99dc40ece255248e6df56cd804b7b556fb7675d4302f48f39a0d11f87f17a9ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823e05bd24824c78e41c5c96c9b9198e4c7dab98438a1bdd1e599b68857f10f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90a991affb6385a3692d158f671f976b6746fdbb9e6b6d0cdda519e047ea4c9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03385a0b0c2ccacfd8f17a6557e6b569870eb0d7645cd5795964a2383e8d8e4b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53baedb5fc12001d3babff86daa092175fce5973f2fa55f066ffc71a7c681c3b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99bc060953e0f2374d33acb1fc8e0f57ee03fba6aa0160a35cb9aadae62bd06a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce0c5baa4449e150378504f77821350b5935a75d596c5cb4a2a07e2a24988e3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketCorsRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9aabf3e975f2fe7427a03fcc25c19443d62d403183caa5c360e0e511d35667(
    *,
    events: typing.Sequence[builtins.str],
    topic: builtins.str,
    filter_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketEventNotificationsFilterRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea39ea2ac1e742899e255c8d72d8654a4082bcdcdf1b83d6689b92acd2249285(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c68cbe19b30f27c5a4a16b32ee61e30245636660d2954d21f2c1e3a1bc31547(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3865a745f2003275528e33c3e06b7958f294e7bbe19c4c420f236981ee1f002f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3dcfbc61fef26447af7fbf6c49d2afd461b3aa2d6338b5ae9f857315ccb6aec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b585f59fc457a53ef9a8ef7f67b86a4001cca235a337955f5415aae0da626a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ef3ccb237e49bce3c6280f9740c2a2afffe1950ab4f56908b405964a6826a9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab234fd5c87d9712aa7f28c314104c828bd12c5bb5d02351f2359b3e5c1068ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketEventNotificationsFilterRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f13fb5d173d0e60bf7e67e535864ffebbc51f66a9487e7618607055e3669268(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e4edd31356174d1c9ae8c65bc9ffe0ac5201eda13ba35c8d6af562fa4ff08be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48845bd6b65242b4d8bc3b0e7594c108bcd944b23d26a42c3dee591d3a0fa5ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef96b45fa712eead14877ae302b170da8f15ca0afd47b3def0b80d894e325e25(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketEventNotificationsFilterRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52cabc61481970bf813f23b1e92b9720312c3f5571c3bb4b12c7d178fd6a6a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8720ca75c7e09c60d3562439429111d8865e12ac6f010c038042d2c1084eb4c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca367a8713aa49071e3629e781a416eb02843846c04165a15fdea9680941cd2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a3e4d3559a4e57044c29d7af12612f9945c84328c24fb8bd2dd197ddce33744(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8832c88b65b3cf36e305ead7242ac2704cbc3314d531568a813c0ad9c69616a8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd99440d3459eaee7d941645e8b05e200f5a771b1667387ff5f099a6edbfe3a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketEventNotifications]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a0952c541475a369567f8365ee3f95cb5650c1faa431dec232e37fa190c393e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0082e9e4c5fd69febd94106f9baf6f33ad17ba3369cecb63dc722cff79c1d9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketEventNotificationsFilterRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3577b019316a7b13556ab2395d34ee4959e079838264bac011f8711bb730ee4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9cb56498229f72e9acbd40d1eb0a9dd35c122eaebb5dc6c6ffdff3d8e4126da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168c6ab0531d8208524cb3b69b4625c1a95e83b62a8f9b57528b57e85a053462(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5b4c7a9c08b5810e7045cccf588a40a0861d2d4dabb03fdb86e1f9e927b0d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketEventNotifications]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8262dd0f5a66cd41547015826014331a7cd0ef68ee54036f9ca6c16820f66d80(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    expiration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRuleExpiration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    noncurrent_version_expiration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRuleNoncurrentVersionExpiration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    noncurrent_version_transition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRuleNoncurrentVersionTransition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    prefix: typing.Optional[builtins.str] = None,
    tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRuleTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
    transition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRuleTransition, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58bf4258df8ac0f4478a72398e0e7e3264298d559b01bc1d6ded1eb6d950f792(
    *,
    days: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb23e1190f5e555ace9580987ea0995944429cc5fb21323b421de9661b6c95f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12aa5f33c8297ee265da6a50e43a6259bc37150fe74a56ed18c971585a25c14(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8df5b12fe3409e76c550db4c81cf449d138b1cc02fae7eb8549c20f364150d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc51cbb1caaa1ea334c96abc43dc057d4280300a6587ae0dd82b742d0a61c23a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a7b64a80d934ee54c658ae18363d2b9a91c0393aeb0348e86997a40545c4b1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273d0b1e249571e838bcdae4a887f038223634cdd49085a01d057eae33fcb9bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleExpiration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9715ec01f7a7d653554aaf5441795b3f80228e8134f84072c803ba910bdc685(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1475fdea07552f08acd2cf1842a054b8fc67b9561441c4d1c5093e50a9792bfe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee2a1fe6414d51359d73b3adb11d052626f121d2ba29a1c4645c7ad03401d78(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleExpiration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6bec10ad7bcad9323907034b9e63d79340386d443872b492405cd82569c271b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d77494ee9860ae487611f8cd8fc355ece6e745334585a297ef54522dd9b933c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b9269cd1f99e17913cd2f7c73fbdfd5b889e7a296cc7db89b339cf18ef4569(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d5fb464e14fb92a59f4e058e3d00c1d78e70fade6e6f67f7797239d2804d04(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda4ce7b85af80fcd922dc558db1614c340361fba0916b74a3322b4af1433877(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f9b23e26e7318e2373f1a7aa133da299b7b030218059f8e1450796edd8e5ce(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1eda33096896a94096508745a24cc184829498ba827d53f048c03e0c717c19b(
    *,
    days: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69936f29c840a9cab9056e4684f72b6d0f53b1049f24b5ea3585b3e04261915d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409d96276b46ca31aca8f62d4b466ed46c2bc935d1cf09f51aa443675d2ca758(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1205a1e4ab77551335b6fe1be464124da616e63185a15ad7e754a64e01e770(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5540fe3a5af8e5c02b10964fc1f2925c846355fe90c6bdf49c634208ddf14151(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2a8377355a727dff84b5e04ba7804d4654b659c07438753d7862be7071eb53(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa5b083507f745b9b95a665b97de6067a355b922fb9f9a6e8cfe6e1d21f54185(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleNoncurrentVersionExpiration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b92f18d2b5590f69f7e2942ee21495e7155459cf03217a1e1da7dcfa14c59db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f9452bc9bb9e3ca955df69346638cc36a93a9dcfcb54302d74939121e10a399(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b7d0b3f9b6947881d70547c62e441d29c64bf796cd498ef56e9b78c569c7c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleNoncurrentVersionExpiration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b8e36cd52dec4814c4ac4e7b53539e42fdb0094aa871cc076c34649f96d8a4(
    *,
    days: jsii.Number,
    storage_class: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5095c91b45f583396758887c7c0db2e0d2c8522675f032838b2ac41a5e6cfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a34d4f82f83bc2de6d2c71c24f91ad30424da5cfb3dccd7e99c32c647b9a5ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5787356d31d6081c04b247f4d01e9af01d6977d172cd68e1362c630fe1a438a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162a3db165c2eab8d88dee179936b34d3699b0cca8c774ad4c08276fcd310a36(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dce15b2bc3be75ab97bc544dff4212419de724ba1ef68bd7b5feadf762ee587(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035e456c37f291318d7827f7b67573cd61b170a6f7620a9f81cc9a3309866ec7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleNoncurrentVersionTransition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31bf2370b118ce2c681444bf899362cdc87a582c9f33771d15a236854947a308(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b5fc48af38eac1189e920a5761ab05e90401d41bdc27722362ad337926b4d8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3bb7415464585cc5ac122616c9c3e2602c6b483e67b9dfad414d5e885bcef8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a6b1aff9adce31eb8bb72936c899b6ee243697400329aff0429dc6d926d057(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleNoncurrentVersionTransition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb01c8682a6b1b26be8ec2c0283ca16e2f3500f689d870a234e0b59e0c8e7a71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3821ce83584c937b53f0bcc62ef93eb25452053bb7543163f9550f4881357051(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRuleExpiration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d488f012a2119ee80659bf3c9003b0aac3fd92904a22e4836ebfb5e70c3b3435(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRuleNoncurrentVersionExpiration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae681cc8dc47163f037d73c0f97176e4b88e81912979cf46bfaf653a2ec417a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRuleNoncurrentVersionTransition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7444f67b894ba2eef11f6ff0c91b0a6e4c06035fe49547e928423f97f52dc250(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRuleTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da7222f2d07b4b1a44f74ec98c71020fb94c907afb273dfdeb93be4938b1a79(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketLifecycleRuleTransition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b09f29d370accb544f5f624d379c367e3e6ecccca42f6e598b24fe1fcca26a27(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d236b1dd86b8ac76c9df9400bb477292abe728a8f8beda60ba2d7c1de9b8698(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507f73ad48072859b5658a75bf9b5d365455108aedd2887392dd5445773e67cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91985d23d0383731fe8fd7261c1a8537ab7347343d927ad3baf586e8d4d169b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e868f1d4924a9c10b1900c2caa4c36fa9f89733be43c49f3858cda220fa2e7(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a254c64fb181cfe89a7dab21134260f7f4803c16d015bb91ddfc130903070d2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f95e9966d3de5b8a8e617c23c2dbd780a0b856a5edd98887486dd91e8afcbfb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f329f134922fe2ba344bba7c33a77bd980817abfad89f44dd472727cdb3ccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2097e1855d6361f063331cda55ec8e58ab2126f32d09e2f43c41feb2a554ce5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aea73bf00d09d9f49c508423dab2dea6400e1b5872c3e3908e365f2d9114be3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de00c98898893be017f20eb219a9713cd0831b69582317614b904ddb78a22b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52692a9a261b87283af580f1ef59f931d72b247e60c3c18efe71a21f56192b2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1c1ef8cbec76827c7e9dd2325758afe269da7dd5da7afc994a6c94687f8ab7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769e882b74e7d51a9bb69fbc1505f06ce46712d28b19fb00213c94a645d2d093(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9821cae8cbe7689b028917950687bc5f362ea7b827569c3e6dd8078f0daf29c4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f5b1de372798966fb45a252f57991d3912b4cf0290752ddfeaba86b7bc29b26(
    *,
    days: jsii.Number,
    storage_class: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e255df9388734dd459d0cb91752836d412d71b35435bbf59e32794e119f59b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__521d15c46e7bf40a8635332233768eabbfb28f16e1a417db6696256b4b6b03d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f8845b564b24de6e151d9ba001202fc125c179ae28423c2729cdd0bb09136f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a09b9d90b6d164614790002c49cbab171516a772f9bce33479c1f7ee1d0801(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82012b85ed196a3a717106a6db67a343c99473ed30203bdbb561ae7107e9602a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c68271d2a0ac7be8de115b29c89bde897fe9cf479ac07015f569d8e833248a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLifecycleRuleTransition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b7ca479111409ae0374c672abf852e2e9fe7447433b14f794980471709e5809(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d086b997092af36749d7c9e05688c59f035481ccd9217ea864be26dc118d03(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11eb374e8a09784c87682327cc99f847803215dcb74e58ef01e950e5e99b9a2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e68df23c9de3258660350ad47bdab31530d4ee82a357110f87f47283f83c392(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLifecycleRuleTransition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faefe30996e057d765d999dc4493309b3d73685bcffb404e659182a483d2161b(
    *,
    target_bucket: builtins.str,
    agency: typing.Optional[builtins.str] = None,
    target_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a082966d7be9102005f602d0aca5ad344082022481c4b5cae3d98685516f8b14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80884a2936f7a3fedd951d4706db4acf4b010273504d67869467c215bbc2ee27(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c195416c491c30915ec07c3e6624de32b5e6332ea50244b0993bdc7d93d77c16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87aa9b40f74cda545380d48382d6551731931a7bd48d4af02651301411dbbad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a7c01c614a23f4d0755180449bbc25200257245e5162150d44ac631a2be0f9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59facc45e2b68bb5caa517e4c3c5506d1f45ef6eec8b1b13fda828fda925a6fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketLogging]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b612f4d8498b47d9ae1405a7fe854df83a4617fc6ceecc74ce69cbb3d9efac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4c1a086f7525e97cc4c7344f99c2c90599a25bd991cc75e405623832b1c1e18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9e4252838b0296d23cb2d2a1aacb5b1b3c12749d1099d21c15870301540942(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d645937f30ae74e3489e2c173ea16ea006f718c5cbbf9bac92972c1e4258f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd26a88df1b5c68c11d9e7ed7292003e8d848f1411e230b953db2d72d6a2a5a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketLogging]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4322da4776a5cd1352d6de284f41d3eaca3cae093f6a5b5ab7f4bd12978d39(
    *,
    algorithm: builtins.str,
    kms_key_id: builtins.str,
    kms_project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae2e8b52d243da387c95129d0487855a15826475bb098ee0d820f45d263a4d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0331f7186898b1b60b7d48b1c6f9d7d11346cbfe66d6ee204bda151504b93bae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48120a022abbf9082a90b03c76e43b85210e14a81ec6ddafc6ade6ddc6dc6952(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf1ada751e585142fdcc2007a04a1b7ef373e1d1c59a6ffdca24b93d9cebe051(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d54b0ce04d544f4e5738886efadabffd5c78bc27981c569ae41f1121b59a3a9(
    value: typing.Optional[ObsBucketServerSideEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f2be9a2a5d3c664a9a1387dd6faf477b0f6af039b239e9f498be43005f9f62(
    *,
    error_document: typing.Optional[builtins.str] = None,
    index_document: typing.Optional[builtins.str] = None,
    redirect_all_requests_to: typing.Optional[builtins.str] = None,
    routing_rules: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a58a526cf7f5181ce525232ed42f04cf130da6834aab329d0b40851b41bca84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4983755d470b097d7d8789f024e13103b0a81df0ccf7974b9b1dbdfeb7691036(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718f02598255b21e8b6b2114256e49c1095040ba62a86f45bf636bb8394d80df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2164a93af8ea029694fa502ca9070ca44f3ef42e935991808b261d050373bf42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8167ece7de8d6fda514e25081932228576955d237f55130036285cc870444d76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be37506e49ca39f6bc87d92b29c66f9df836ff7322b432b63867eb7d26e5709(
    value: typing.Optional[ObsBucketWebsite],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063731e4b5f1c7078cb9399e808475e3bf068d0867e38b4e42d42cb281b97f6d(
    *,
    days: typing.Optional[jsii.Number] = None,
    years: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f1cc00240e2d13466ca484bf9fbbdde4405927408f1adcbe1b00c209b6457a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9f1bbdc509502add69dd55b0bac071b57b6552f5ad324ec81ec1b71f0c5047(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdcbf0a9cc23aaab7b2be21622acfd79f522d551db17cdbd1ce817be25bdc522(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc25460aa918dd26e4a9c1e76b383467588ab7b12e55b957cc45c822133b68ab(
    value: typing.Optional[ObsBucketWormPolicy],
) -> None:
    """Type checking stubs"""
    pass
