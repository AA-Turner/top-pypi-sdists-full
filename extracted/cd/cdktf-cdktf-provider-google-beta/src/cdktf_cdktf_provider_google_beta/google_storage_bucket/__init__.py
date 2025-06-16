r'''
# `google_storage_bucket`

Refer to the Terraform Registry for docs: [`google_storage_bucket`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket).
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


class GoogleStorageBucket(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucket",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket google_storage_bucket}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        autoclass: typing.Optional[typing.Union["GoogleStorageBucketAutoclass", typing.Dict[builtins.str, typing.Any]]] = None,
        cors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleStorageBucketCors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_placement_config: typing.Optional[typing.Union["GoogleStorageBucketCustomPlacementConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_event_based_hold: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_object_retention: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption: typing.Optional[typing.Union["GoogleStorageBucketEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hierarchical_namespace: typing.Optional[typing.Union["GoogleStorageBucketHierarchicalNamespace", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_filter: typing.Optional[typing.Union["GoogleStorageBucketIpFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleStorageBucketLifecycleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        logging: typing.Optional[typing.Union["GoogleStorageBucketLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        public_access_prevention: typing.Optional[builtins.str] = None,
        requester_pays: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_policy: typing.Optional[typing.Union["GoogleStorageBucketRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        rpo: typing.Optional[builtins.str] = None,
        soft_delete_policy: typing.Optional[typing.Union["GoogleStorageBucketSoftDeletePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_class: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleStorageBucketTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        uniform_bucket_level_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        versioning: typing.Optional[typing.Union["GoogleStorageBucketVersioning", typing.Dict[builtins.str, typing.Any]]] = None,
        website: typing.Optional[typing.Union["GoogleStorageBucketWebsite", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket google_storage_bucket} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The Google Cloud Storage location or region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#location GoogleStorageBucket#location}
        :param name: The name of the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#name GoogleStorageBucket#name}
        :param autoclass: autoclass block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#autoclass GoogleStorageBucket#autoclass}
        :param cors: cors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#cors GoogleStorageBucket#cors}
        :param custom_placement_config: custom_placement_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#custom_placement_config GoogleStorageBucket#custom_placement_config}
        :param default_event_based_hold: Whether or not to automatically apply an eventBasedHold to new objects added to the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#default_event_based_hold GoogleStorageBucket#default_event_based_hold}
        :param enable_object_retention: Enables each object in the bucket to have its own retention policy, which prevents deletion until stored for a specific length of time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#enable_object_retention GoogleStorageBucket#enable_object_retention}
        :param encryption: encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#encryption GoogleStorageBucket#encryption}
        :param force_destroy: When deleting a bucket, this boolean option will delete all contained objects, or anywhereCaches (if any). If you try to delete a bucket that contains objects or anywhereCaches, Terraform will fail that run, deleting anywhereCaches may take 80 minutes to complete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#force_destroy GoogleStorageBucket#force_destroy}
        :param hierarchical_namespace: hierarchical_namespace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#hierarchical_namespace GoogleStorageBucket#hierarchical_namespace}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#id GoogleStorageBucket#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_filter: ip_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#ip_filter GoogleStorageBucket#ip_filter}
        :param labels: A set of key/value label pairs to assign to the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#labels GoogleStorageBucket#labels}
        :param lifecycle_rule: lifecycle_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#lifecycle_rule GoogleStorageBucket#lifecycle_rule}
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#logging GoogleStorageBucket#logging}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#project GoogleStorageBucket#project}
        :param public_access_prevention: Prevents public access to a bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#public_access_prevention GoogleStorageBucket#public_access_prevention}
        :param requester_pays: Enables Requester Pays on a storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#requester_pays GoogleStorageBucket#requester_pays}
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#retention_policy GoogleStorageBucket#retention_policy}
        :param rpo: Specifies the RPO setting of bucket. If set 'ASYNC_TURBO', The Turbo Replication will be enabled for the dual-region bucket. Value 'DEFAULT' will set RPO setting to default. Turbo Replication is only for buckets in dual-regions.See the docs for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#rpo GoogleStorageBucket#rpo}
        :param soft_delete_policy: soft_delete_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#soft_delete_policy GoogleStorageBucket#soft_delete_policy}
        :param storage_class: The Storage Class of the new bucket. Supported values include: STANDARD, MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#storage_class GoogleStorageBucket#storage_class}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#timeouts GoogleStorageBucket#timeouts}
        :param uniform_bucket_level_access: Enables uniform bucket-level access on a bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#uniform_bucket_level_access GoogleStorageBucket#uniform_bucket_level_access}
        :param versioning: versioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#versioning GoogleStorageBucket#versioning}
        :param website: website block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#website GoogleStorageBucket#website}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96b01c7750cdefb3fba97844d4f02a4010e6bcb00ea6e5f27e6cea37c7f6e28)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleStorageBucketConfig(
            location=location,
            name=name,
            autoclass=autoclass,
            cors=cors,
            custom_placement_config=custom_placement_config,
            default_event_based_hold=default_event_based_hold,
            enable_object_retention=enable_object_retention,
            encryption=encryption,
            force_destroy=force_destroy,
            hierarchical_namespace=hierarchical_namespace,
            id=id,
            ip_filter=ip_filter,
            labels=labels,
            lifecycle_rule=lifecycle_rule,
            logging=logging,
            project=project,
            public_access_prevention=public_access_prevention,
            requester_pays=requester_pays,
            retention_policy=retention_policy,
            rpo=rpo,
            soft_delete_policy=soft_delete_policy,
            storage_class=storage_class,
            timeouts=timeouts,
            uniform_bucket_level_access=uniform_bucket_level_access,
            versioning=versioning,
            website=website,
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
        '''Generates CDKTF code for importing a GoogleStorageBucket resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleStorageBucket to import.
        :param import_from_id: The id of the existing GoogleStorageBucket that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleStorageBucket to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8199978729f9d2216be606073c97cbf214d839092f96b450d40c00e3c89311)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoclass")
    def put_autoclass(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        terminal_storage_class: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: While set to true, autoclass automatically transitions objects in your bucket to appropriate storage classes based on each object's access pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#enabled GoogleStorageBucket#enabled}
        :param terminal_storage_class: The storage class that objects in the bucket eventually transition to if they are not read for a certain length of time. Supported values include: NEARLINE, ARCHIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#terminal_storage_class GoogleStorageBucket#terminal_storage_class}
        '''
        value = GoogleStorageBucketAutoclass(
            enabled=enabled, terminal_storage_class=terminal_storage_class
        )

        return typing.cast(None, jsii.invoke(self, "putAutoclass", [value]))

    @jsii.member(jsii_name="putCors")
    def put_cors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleStorageBucketCors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86dc3c42f9665643610073bdacf287de6f68ca9daa71c8ecf04d6d6694a972c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCors", [value]))

    @jsii.member(jsii_name="putCustomPlacementConfig")
    def put_custom_placement_config(
        self,
        *,
        data_locations: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param data_locations: The list of individual regions that comprise a dual-region bucket. See the docs for a list of acceptable regions. Note: If any of the data_locations changes, it will recreate the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#data_locations GoogleStorageBucket#data_locations}
        '''
        value = GoogleStorageBucketCustomPlacementConfig(data_locations=data_locations)

        return typing.cast(None, jsii.invoke(self, "putCustomPlacementConfig", [value]))

    @jsii.member(jsii_name="putEncryption")
    def put_encryption(self, *, default_kms_key_name: builtins.str) -> None:
        '''
        :param default_kms_key_name: A Cloud KMS key that will be used to encrypt objects inserted into this bucket, if no encryption method is specified. You must pay attention to whether the crypto key is available in the location that this bucket is created in. See the docs for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#default_kms_key_name GoogleStorageBucket#default_kms_key_name}
        '''
        value = GoogleStorageBucketEncryption(
            default_kms_key_name=default_kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putEncryption", [value]))

    @jsii.member(jsii_name="putHierarchicalNamespace")
    def put_hierarchical_namespace(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Set this field true to organize bucket with logical file system structure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#enabled GoogleStorageBucket#enabled}
        '''
        value = GoogleStorageBucketHierarchicalNamespace(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putHierarchicalNamespace", [value]))

    @jsii.member(jsii_name="putIpFilter")
    def put_ip_filter(
        self,
        *,
        mode: builtins.str,
        public_network_source: typing.Optional[typing.Union["GoogleStorageBucketIpFilterPublicNetworkSource", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_network_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleStorageBucketIpFilterVpcNetworkSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param mode: The mode of the IP filter. Valid values are 'Enabled' and 'Disabled'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#mode GoogleStorageBucket#mode}
        :param public_network_source: public_network_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#public_network_source GoogleStorageBucket#public_network_source}
        :param vpc_network_sources: vpc_network_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#vpc_network_sources GoogleStorageBucket#vpc_network_sources}
        '''
        value = GoogleStorageBucketIpFilter(
            mode=mode,
            public_network_source=public_network_source,
            vpc_network_sources=vpc_network_sources,
        )

        return typing.cast(None, jsii.invoke(self, "putIpFilter", [value]))

    @jsii.member(jsii_name="putLifecycleRule")
    def put_lifecycle_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleStorageBucketLifecycleRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56d85c194504e5578dcb0bc3b72c80b9882370c23fdd6440c7d90a3e9688373f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLifecycleRule", [value]))

    @jsii.member(jsii_name="putLogging")
    def put_logging(
        self,
        *,
        log_bucket: builtins.str,
        log_object_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_bucket: The bucket that will receive log objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#log_bucket GoogleStorageBucket#log_bucket}
        :param log_object_prefix: The object prefix for log objects. If it's not provided, by default Google Cloud Storage sets this to this bucket's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#log_object_prefix GoogleStorageBucket#log_object_prefix}
        '''
        value = GoogleStorageBucketLogging(
            log_bucket=log_bucket, log_object_prefix=log_object_prefix
        )

        return typing.cast(None, jsii.invoke(self, "putLogging", [value]))

    @jsii.member(jsii_name="putRetentionPolicy")
    def put_retention_policy(
        self,
        *,
        retention_period: jsii.Number,
        is_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param retention_period: The period of time, in seconds, that objects in the bucket must be retained and cannot be deleted, overwritten, or archived. The value must be less than 3,155,760,000 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#retention_period GoogleStorageBucket#retention_period}
        :param is_locked: If set to true, the bucket will be locked and permanently restrict edits to the bucket's retention policy. Caution: Locking a bucket is an irreversible action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#is_locked GoogleStorageBucket#is_locked}
        '''
        value = GoogleStorageBucketRetentionPolicy(
            retention_period=retention_period, is_locked=is_locked
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionPolicy", [value]))

    @jsii.member(jsii_name="putSoftDeletePolicy")
    def put_soft_delete_policy(
        self,
        *,
        retention_duration_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param retention_duration_seconds: The duration in seconds that soft-deleted objects in the bucket will be retained and cannot be permanently deleted. Default value is 604800. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#retention_duration_seconds GoogleStorageBucket#retention_duration_seconds}
        '''
        value = GoogleStorageBucketSoftDeletePolicy(
            retention_duration_seconds=retention_duration_seconds
        )

        return typing.cast(None, jsii.invoke(self, "putSoftDeletePolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#create GoogleStorageBucket#create}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#read GoogleStorageBucket#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#update GoogleStorageBucket#update}.
        '''
        value = GoogleStorageBucketTimeouts(create=create, read=read, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVersioning")
    def put_versioning(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: While set to true, versioning is fully enabled for this bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#enabled GoogleStorageBucket#enabled}
        '''
        value = GoogleStorageBucketVersioning(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putVersioning", [value]))

    @jsii.member(jsii_name="putWebsite")
    def put_website(
        self,
        *,
        main_page_suffix: typing.Optional[builtins.str] = None,
        not_found_page: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param main_page_suffix: Behaves as the bucket's directory index where missing objects are treated as potential directories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#main_page_suffix GoogleStorageBucket#main_page_suffix}
        :param not_found_page: The custom object to return when a requested resource is not found. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#not_found_page GoogleStorageBucket#not_found_page}
        '''
        value = GoogleStorageBucketWebsite(
            main_page_suffix=main_page_suffix, not_found_page=not_found_page
        )

        return typing.cast(None, jsii.invoke(self, "putWebsite", [value]))

    @jsii.member(jsii_name="resetAutoclass")
    def reset_autoclass(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoclass", []))

    @jsii.member(jsii_name="resetCors")
    def reset_cors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCors", []))

    @jsii.member(jsii_name="resetCustomPlacementConfig")
    def reset_custom_placement_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomPlacementConfig", []))

    @jsii.member(jsii_name="resetDefaultEventBasedHold")
    def reset_default_event_based_hold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultEventBasedHold", []))

    @jsii.member(jsii_name="resetEnableObjectRetention")
    def reset_enable_object_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableObjectRetention", []))

    @jsii.member(jsii_name="resetEncryption")
    def reset_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryption", []))

    @jsii.member(jsii_name="resetForceDestroy")
    def reset_force_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDestroy", []))

    @jsii.member(jsii_name="resetHierarchicalNamespace")
    def reset_hierarchical_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHierarchicalNamespace", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpFilter")
    def reset_ip_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpFilter", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLifecycleRule")
    def reset_lifecycle_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleRule", []))

    @jsii.member(jsii_name="resetLogging")
    def reset_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogging", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPublicAccessPrevention")
    def reset_public_access_prevention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicAccessPrevention", []))

    @jsii.member(jsii_name="resetRequesterPays")
    def reset_requester_pays(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequesterPays", []))

    @jsii.member(jsii_name="resetRetentionPolicy")
    def reset_retention_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicy", []))

    @jsii.member(jsii_name="resetRpo")
    def reset_rpo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRpo", []))

    @jsii.member(jsii_name="resetSoftDeletePolicy")
    def reset_soft_delete_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSoftDeletePolicy", []))

    @jsii.member(jsii_name="resetStorageClass")
    def reset_storage_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageClass", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUniformBucketLevelAccess")
    def reset_uniform_bucket_level_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUniformBucketLevelAccess", []))

    @jsii.member(jsii_name="resetVersioning")
    def reset_versioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersioning", []))

    @jsii.member(jsii_name="resetWebsite")
    def reset_website(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebsite", []))

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
    @jsii.member(jsii_name="autoclass")
    def autoclass(self) -> "GoogleStorageBucketAutoclassOutputReference":
        return typing.cast("GoogleStorageBucketAutoclassOutputReference", jsii.get(self, "autoclass"))

    @builtins.property
    @jsii.member(jsii_name="cors")
    def cors(self) -> "GoogleStorageBucketCorsList":
        return typing.cast("GoogleStorageBucketCorsList", jsii.get(self, "cors"))

    @builtins.property
    @jsii.member(jsii_name="customPlacementConfig")
    def custom_placement_config(
        self,
    ) -> "GoogleStorageBucketCustomPlacementConfigOutputReference":
        return typing.cast("GoogleStorageBucketCustomPlacementConfigOutputReference", jsii.get(self, "customPlacementConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="encryption")
    def encryption(self) -> "GoogleStorageBucketEncryptionOutputReference":
        return typing.cast("GoogleStorageBucketEncryptionOutputReference", jsii.get(self, "encryption"))

    @builtins.property
    @jsii.member(jsii_name="hierarchicalNamespace")
    def hierarchical_namespace(
        self,
    ) -> "GoogleStorageBucketHierarchicalNamespaceOutputReference":
        return typing.cast("GoogleStorageBucketHierarchicalNamespaceOutputReference", jsii.get(self, "hierarchicalNamespace"))

    @builtins.property
    @jsii.member(jsii_name="ipFilter")
    def ip_filter(self) -> "GoogleStorageBucketIpFilterOutputReference":
        return typing.cast("GoogleStorageBucketIpFilterOutputReference", jsii.get(self, "ipFilter"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleRule")
    def lifecycle_rule(self) -> "GoogleStorageBucketLifecycleRuleList":
        return typing.cast("GoogleStorageBucketLifecycleRuleList", jsii.get(self, "lifecycleRule"))

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> "GoogleStorageBucketLoggingOutputReference":
        return typing.cast("GoogleStorageBucketLoggingOutputReference", jsii.get(self, "logging"))

    @builtins.property
    @jsii.member(jsii_name="projectNumber")
    def project_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "projectNumber"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(self) -> "GoogleStorageBucketRetentionPolicyOutputReference":
        return typing.cast("GoogleStorageBucketRetentionPolicyOutputReference", jsii.get(self, "retentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="softDeletePolicy")
    def soft_delete_policy(
        self,
    ) -> "GoogleStorageBucketSoftDeletePolicyOutputReference":
        return typing.cast("GoogleStorageBucketSoftDeletePolicyOutputReference", jsii.get(self, "softDeletePolicy"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeCreated")
    def time_created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeCreated"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleStorageBucketTimeoutsOutputReference":
        return typing.cast("GoogleStorageBucketTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updated")
    def updated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updated"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="versioning")
    def versioning(self) -> "GoogleStorageBucketVersioningOutputReference":
        return typing.cast("GoogleStorageBucketVersioningOutputReference", jsii.get(self, "versioning"))

    @builtins.property
    @jsii.member(jsii_name="website")
    def website(self) -> "GoogleStorageBucketWebsiteOutputReference":
        return typing.cast("GoogleStorageBucketWebsiteOutputReference", jsii.get(self, "website"))

    @builtins.property
    @jsii.member(jsii_name="autoclassInput")
    def autoclass_input(self) -> typing.Optional["GoogleStorageBucketAutoclass"]:
        return typing.cast(typing.Optional["GoogleStorageBucketAutoclass"], jsii.get(self, "autoclassInput"))

    @builtins.property
    @jsii.member(jsii_name="corsInput")
    def cors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageBucketCors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageBucketCors"]]], jsii.get(self, "corsInput"))

    @builtins.property
    @jsii.member(jsii_name="customPlacementConfigInput")
    def custom_placement_config_input(
        self,
    ) -> typing.Optional["GoogleStorageBucketCustomPlacementConfig"]:
        return typing.cast(typing.Optional["GoogleStorageBucketCustomPlacementConfig"], jsii.get(self, "customPlacementConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultEventBasedHoldInput")
    def default_event_based_hold_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultEventBasedHoldInput"))

    @builtins.property
    @jsii.member(jsii_name="enableObjectRetentionInput")
    def enable_object_retention_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableObjectRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionInput")
    def encryption_input(self) -> typing.Optional["GoogleStorageBucketEncryption"]:
        return typing.cast(typing.Optional["GoogleStorageBucketEncryption"], jsii.get(self, "encryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDestroyInput")
    def force_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="hierarchicalNamespaceInput")
    def hierarchical_namespace_input(
        self,
    ) -> typing.Optional["GoogleStorageBucketHierarchicalNamespace"]:
        return typing.cast(typing.Optional["GoogleStorageBucketHierarchicalNamespace"], jsii.get(self, "hierarchicalNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipFilterInput")
    def ip_filter_input(self) -> typing.Optional["GoogleStorageBucketIpFilter"]:
        return typing.cast(typing.Optional["GoogleStorageBucketIpFilter"], jsii.get(self, "ipFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleRuleInput")
    def lifecycle_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageBucketLifecycleRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageBucketLifecycleRule"]]], jsii.get(self, "lifecycleRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(self) -> typing.Optional["GoogleStorageBucketLogging"]:
        return typing.cast(typing.Optional["GoogleStorageBucketLogging"], jsii.get(self, "loggingInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="publicAccessPreventionInput")
    def public_access_prevention_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicAccessPreventionInput"))

    @builtins.property
    @jsii.member(jsii_name="requesterPaysInput")
    def requester_pays_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requesterPaysInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyInput")
    def retention_policy_input(
        self,
    ) -> typing.Optional["GoogleStorageBucketRetentionPolicy"]:
        return typing.cast(typing.Optional["GoogleStorageBucketRetentionPolicy"], jsii.get(self, "retentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="rpoInput")
    def rpo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rpoInput"))

    @builtins.property
    @jsii.member(jsii_name="softDeletePolicyInput")
    def soft_delete_policy_input(
        self,
    ) -> typing.Optional["GoogleStorageBucketSoftDeletePolicy"]:
        return typing.cast(typing.Optional["GoogleStorageBucketSoftDeletePolicy"], jsii.get(self, "softDeletePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="storageClassInput")
    def storage_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleStorageBucketTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleStorageBucketTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="uniformBucketLevelAccessInput")
    def uniform_bucket_level_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "uniformBucketLevelAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="versioningInput")
    def versioning_input(self) -> typing.Optional["GoogleStorageBucketVersioning"]:
        return typing.cast(typing.Optional["GoogleStorageBucketVersioning"], jsii.get(self, "versioningInput"))

    @builtins.property
    @jsii.member(jsii_name="websiteInput")
    def website_input(self) -> typing.Optional["GoogleStorageBucketWebsite"]:
        return typing.cast(typing.Optional["GoogleStorageBucketWebsite"], jsii.get(self, "websiteInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultEventBasedHold")
    def default_event_based_hold(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultEventBasedHold"))

    @default_event_based_hold.setter
    def default_event_based_hold(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__534bb0e91dcdf26648981490ff48446eb6747b98609a9399c0248c41a39e3987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultEventBasedHold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableObjectRetention")
    def enable_object_retention(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableObjectRetention"))

    @enable_object_retention.setter
    def enable_object_retention(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5655ef99ccd361bcbd45b9f62e262cbec97e97c0467c065743c9f69bed645bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableObjectRetention", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__3037e124abb7cd3a7a5b7d7667a52809eb628386d78da504fb43b05a4642a33b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0863af05a34e34384a3fecedfd0a74c96fd2897e7dbe2ab0b942a85f5ae83232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9da57b75f3e411ca65a3304f309d00a97f4bf72e118914d4c98d42eec260fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a05b8eb66bf2544a271ac0bf7706868f6e357468ac21fc8e895e3319e1f67f75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9561046b88c653b419817d6e197f342b6637ecdb2c559f50f36e8baba7e2b73a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58f15dac6100a76cd00c99d6479a0e498419e427bb137c4464c4deb8bbe3d468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicAccessPrevention")
    def public_access_prevention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicAccessPrevention"))

    @public_access_prevention.setter
    def public_access_prevention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b4302fccb6f81a5e30afa6c06063f970a9087e1bfad15d668ed333ea292570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicAccessPrevention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requesterPays")
    def requester_pays(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requesterPays"))

    @requester_pays.setter
    def requester_pays(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19086bcdeb6b2a3c97427819dfff62b5e381ef3d8e5620690e4d6bbcbe911a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requesterPays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rpo")
    def rpo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rpo"))

    @rpo.setter
    def rpo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fefd0e6c984446e81222637dc9cbf800fc2d2a6db4b994d5ce11dcc31b4b38f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rpo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a68a1710af04cdcd3cdb188187b334d83b5a46427d6cfed40061ead17a00f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uniformBucketLevelAccess")
    def uniform_bucket_level_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "uniformBucketLevelAccess"))

    @uniform_bucket_level_access.setter
    def uniform_bucket_level_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f0228bad12bec8950e878585ca6c609ebb135ce00c4a4921a601dffe5f88e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uniformBucketLevelAccess", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketAutoclass",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "terminal_storage_class": "terminalStorageClass",
    },
)
class GoogleStorageBucketAutoclass:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        terminal_storage_class: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: While set to true, autoclass automatically transitions objects in your bucket to appropriate storage classes based on each object's access pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#enabled GoogleStorageBucket#enabled}
        :param terminal_storage_class: The storage class that objects in the bucket eventually transition to if they are not read for a certain length of time. Supported values include: NEARLINE, ARCHIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#terminal_storage_class GoogleStorageBucket#terminal_storage_class}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1d333df0da0eb61948e89deb3c0d6ca6110864821ee392602744ef26ef03f3)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument terminal_storage_class", value=terminal_storage_class, expected_type=type_hints["terminal_storage_class"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if terminal_storage_class is not None:
            self._values["terminal_storage_class"] = terminal_storage_class

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''While set to true, autoclass automatically transitions objects in your bucket to appropriate storage classes based on each object's access pattern.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#enabled GoogleStorageBucket#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def terminal_storage_class(self) -> typing.Optional[builtins.str]:
        '''The storage class that objects in the bucket eventually transition to if they are not read for a certain length of time.

        Supported values include: NEARLINE, ARCHIVE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#terminal_storage_class GoogleStorageBucket#terminal_storage_class}
        '''
        result = self._values.get("terminal_storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketAutoclass(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketAutoclassOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketAutoclassOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdcafb7b1f73587c4e444f55434d9b6bbe14be1562382704f19f4430100f0256)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTerminalStorageClass")
    def reset_terminal_storage_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminalStorageClass", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="terminalStorageClassInput")
    def terminal_storage_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "terminalStorageClassInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c5bdbe11e4ed1f582a872fa13417b3a4d29ff9c05286bc4dae706cd65707e574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminalStorageClass")
    def terminal_storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terminalStorageClass"))

    @terminal_storage_class.setter
    def terminal_storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d913e77ab6c610fda8613945514134abca3d37e08d6486cea2c5e4f032bcaaa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminalStorageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleStorageBucketAutoclass]:
        return typing.cast(typing.Optional[GoogleStorageBucketAutoclass], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBucketAutoclass],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7611b557e9b3825a4332fad225343cc5021bfae6f3e8a1e486bc41760d7cf426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "autoclass": "autoclass",
        "cors": "cors",
        "custom_placement_config": "customPlacementConfig",
        "default_event_based_hold": "defaultEventBasedHold",
        "enable_object_retention": "enableObjectRetention",
        "encryption": "encryption",
        "force_destroy": "forceDestroy",
        "hierarchical_namespace": "hierarchicalNamespace",
        "id": "id",
        "ip_filter": "ipFilter",
        "labels": "labels",
        "lifecycle_rule": "lifecycleRule",
        "logging": "logging",
        "project": "project",
        "public_access_prevention": "publicAccessPrevention",
        "requester_pays": "requesterPays",
        "retention_policy": "retentionPolicy",
        "rpo": "rpo",
        "soft_delete_policy": "softDeletePolicy",
        "storage_class": "storageClass",
        "timeouts": "timeouts",
        "uniform_bucket_level_access": "uniformBucketLevelAccess",
        "versioning": "versioning",
        "website": "website",
    },
)
class GoogleStorageBucketConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        autoclass: typing.Optional[typing.Union[GoogleStorageBucketAutoclass, typing.Dict[builtins.str, typing.Any]]] = None,
        cors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleStorageBucketCors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_placement_config: typing.Optional[typing.Union["GoogleStorageBucketCustomPlacementConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_event_based_hold: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_object_retention: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption: typing.Optional[typing.Union["GoogleStorageBucketEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hierarchical_namespace: typing.Optional[typing.Union["GoogleStorageBucketHierarchicalNamespace", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_filter: typing.Optional[typing.Union["GoogleStorageBucketIpFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleStorageBucketLifecycleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        logging: typing.Optional[typing.Union["GoogleStorageBucketLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        public_access_prevention: typing.Optional[builtins.str] = None,
        requester_pays: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_policy: typing.Optional[typing.Union["GoogleStorageBucketRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        rpo: typing.Optional[builtins.str] = None,
        soft_delete_policy: typing.Optional[typing.Union["GoogleStorageBucketSoftDeletePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_class: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleStorageBucketTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        uniform_bucket_level_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        versioning: typing.Optional[typing.Union["GoogleStorageBucketVersioning", typing.Dict[builtins.str, typing.Any]]] = None,
        website: typing.Optional[typing.Union["GoogleStorageBucketWebsite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The Google Cloud Storage location or region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#location GoogleStorageBucket#location}
        :param name: The name of the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#name GoogleStorageBucket#name}
        :param autoclass: autoclass block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#autoclass GoogleStorageBucket#autoclass}
        :param cors: cors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#cors GoogleStorageBucket#cors}
        :param custom_placement_config: custom_placement_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#custom_placement_config GoogleStorageBucket#custom_placement_config}
        :param default_event_based_hold: Whether or not to automatically apply an eventBasedHold to new objects added to the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#default_event_based_hold GoogleStorageBucket#default_event_based_hold}
        :param enable_object_retention: Enables each object in the bucket to have its own retention policy, which prevents deletion until stored for a specific length of time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#enable_object_retention GoogleStorageBucket#enable_object_retention}
        :param encryption: encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#encryption GoogleStorageBucket#encryption}
        :param force_destroy: When deleting a bucket, this boolean option will delete all contained objects, or anywhereCaches (if any). If you try to delete a bucket that contains objects or anywhereCaches, Terraform will fail that run, deleting anywhereCaches may take 80 minutes to complete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#force_destroy GoogleStorageBucket#force_destroy}
        :param hierarchical_namespace: hierarchical_namespace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#hierarchical_namespace GoogleStorageBucket#hierarchical_namespace}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#id GoogleStorageBucket#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_filter: ip_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#ip_filter GoogleStorageBucket#ip_filter}
        :param labels: A set of key/value label pairs to assign to the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#labels GoogleStorageBucket#labels}
        :param lifecycle_rule: lifecycle_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#lifecycle_rule GoogleStorageBucket#lifecycle_rule}
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#logging GoogleStorageBucket#logging}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#project GoogleStorageBucket#project}
        :param public_access_prevention: Prevents public access to a bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#public_access_prevention GoogleStorageBucket#public_access_prevention}
        :param requester_pays: Enables Requester Pays on a storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#requester_pays GoogleStorageBucket#requester_pays}
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#retention_policy GoogleStorageBucket#retention_policy}
        :param rpo: Specifies the RPO setting of bucket. If set 'ASYNC_TURBO', The Turbo Replication will be enabled for the dual-region bucket. Value 'DEFAULT' will set RPO setting to default. Turbo Replication is only for buckets in dual-regions.See the docs for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#rpo GoogleStorageBucket#rpo}
        :param soft_delete_policy: soft_delete_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#soft_delete_policy GoogleStorageBucket#soft_delete_policy}
        :param storage_class: The Storage Class of the new bucket. Supported values include: STANDARD, MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#storage_class GoogleStorageBucket#storage_class}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#timeouts GoogleStorageBucket#timeouts}
        :param uniform_bucket_level_access: Enables uniform bucket-level access on a bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#uniform_bucket_level_access GoogleStorageBucket#uniform_bucket_level_access}
        :param versioning: versioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#versioning GoogleStorageBucket#versioning}
        :param website: website block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#website GoogleStorageBucket#website}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoclass, dict):
            autoclass = GoogleStorageBucketAutoclass(**autoclass)
        if isinstance(custom_placement_config, dict):
            custom_placement_config = GoogleStorageBucketCustomPlacementConfig(**custom_placement_config)
        if isinstance(encryption, dict):
            encryption = GoogleStorageBucketEncryption(**encryption)
        if isinstance(hierarchical_namespace, dict):
            hierarchical_namespace = GoogleStorageBucketHierarchicalNamespace(**hierarchical_namespace)
        if isinstance(ip_filter, dict):
            ip_filter = GoogleStorageBucketIpFilter(**ip_filter)
        if isinstance(logging, dict):
            logging = GoogleStorageBucketLogging(**logging)
        if isinstance(retention_policy, dict):
            retention_policy = GoogleStorageBucketRetentionPolicy(**retention_policy)
        if isinstance(soft_delete_policy, dict):
            soft_delete_policy = GoogleStorageBucketSoftDeletePolicy(**soft_delete_policy)
        if isinstance(timeouts, dict):
            timeouts = GoogleStorageBucketTimeouts(**timeouts)
        if isinstance(versioning, dict):
            versioning = GoogleStorageBucketVersioning(**versioning)
        if isinstance(website, dict):
            website = GoogleStorageBucketWebsite(**website)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3623721f62b375d44511fb3c7e51f92199d618059b7a77a5062075147e8cae2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument autoclass", value=autoclass, expected_type=type_hints["autoclass"])
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument custom_placement_config", value=custom_placement_config, expected_type=type_hints["custom_placement_config"])
            check_type(argname="argument default_event_based_hold", value=default_event_based_hold, expected_type=type_hints["default_event_based_hold"])
            check_type(argname="argument enable_object_retention", value=enable_object_retention, expected_type=type_hints["enable_object_retention"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument force_destroy", value=force_destroy, expected_type=type_hints["force_destroy"])
            check_type(argname="argument hierarchical_namespace", value=hierarchical_namespace, expected_type=type_hints["hierarchical_namespace"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_filter", value=ip_filter, expected_type=type_hints["ip_filter"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument lifecycle_rule", value=lifecycle_rule, expected_type=type_hints["lifecycle_rule"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument public_access_prevention", value=public_access_prevention, expected_type=type_hints["public_access_prevention"])
            check_type(argname="argument requester_pays", value=requester_pays, expected_type=type_hints["requester_pays"])
            check_type(argname="argument retention_policy", value=retention_policy, expected_type=type_hints["retention_policy"])
            check_type(argname="argument rpo", value=rpo, expected_type=type_hints["rpo"])
            check_type(argname="argument soft_delete_policy", value=soft_delete_policy, expected_type=type_hints["soft_delete_policy"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument uniform_bucket_level_access", value=uniform_bucket_level_access, expected_type=type_hints["uniform_bucket_level_access"])
            check_type(argname="argument versioning", value=versioning, expected_type=type_hints["versioning"])
            check_type(argname="argument website", value=website, expected_type=type_hints["website"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
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
        if autoclass is not None:
            self._values["autoclass"] = autoclass
        if cors is not None:
            self._values["cors"] = cors
        if custom_placement_config is not None:
            self._values["custom_placement_config"] = custom_placement_config
        if default_event_based_hold is not None:
            self._values["default_event_based_hold"] = default_event_based_hold
        if enable_object_retention is not None:
            self._values["enable_object_retention"] = enable_object_retention
        if encryption is not None:
            self._values["encryption"] = encryption
        if force_destroy is not None:
            self._values["force_destroy"] = force_destroy
        if hierarchical_namespace is not None:
            self._values["hierarchical_namespace"] = hierarchical_namespace
        if id is not None:
            self._values["id"] = id
        if ip_filter is not None:
            self._values["ip_filter"] = ip_filter
        if labels is not None:
            self._values["labels"] = labels
        if lifecycle_rule is not None:
            self._values["lifecycle_rule"] = lifecycle_rule
        if logging is not None:
            self._values["logging"] = logging
        if project is not None:
            self._values["project"] = project
        if public_access_prevention is not None:
            self._values["public_access_prevention"] = public_access_prevention
        if requester_pays is not None:
            self._values["requester_pays"] = requester_pays
        if retention_policy is not None:
            self._values["retention_policy"] = retention_policy
        if rpo is not None:
            self._values["rpo"] = rpo
        if soft_delete_policy is not None:
            self._values["soft_delete_policy"] = soft_delete_policy
        if storage_class is not None:
            self._values["storage_class"] = storage_class
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if uniform_bucket_level_access is not None:
            self._values["uniform_bucket_level_access"] = uniform_bucket_level_access
        if versioning is not None:
            self._values["versioning"] = versioning
        if website is not None:
            self._values["website"] = website

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
    def location(self) -> builtins.str:
        '''The Google Cloud Storage location or region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#location GoogleStorageBucket#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#name GoogleStorageBucket#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoclass(self) -> typing.Optional[GoogleStorageBucketAutoclass]:
        '''autoclass block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#autoclass GoogleStorageBucket#autoclass}
        '''
        result = self._values.get("autoclass")
        return typing.cast(typing.Optional[GoogleStorageBucketAutoclass], result)

    @builtins.property
    def cors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageBucketCors"]]]:
        '''cors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#cors GoogleStorageBucket#cors}
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageBucketCors"]]], result)

    @builtins.property
    def custom_placement_config(
        self,
    ) -> typing.Optional["GoogleStorageBucketCustomPlacementConfig"]:
        '''custom_placement_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#custom_placement_config GoogleStorageBucket#custom_placement_config}
        '''
        result = self._values.get("custom_placement_config")
        return typing.cast(typing.Optional["GoogleStorageBucketCustomPlacementConfig"], result)

    @builtins.property
    def default_event_based_hold(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not to automatically apply an eventBasedHold to new objects added to the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#default_event_based_hold GoogleStorageBucket#default_event_based_hold}
        '''
        result = self._values.get("default_event_based_hold")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_object_retention(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables each object in the bucket to have its own retention policy, which prevents deletion until stored for a specific length of time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#enable_object_retention GoogleStorageBucket#enable_object_retention}
        '''
        result = self._values.get("enable_object_retention")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption(self) -> typing.Optional["GoogleStorageBucketEncryption"]:
        '''encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#encryption GoogleStorageBucket#encryption}
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional["GoogleStorageBucketEncryption"], result)

    @builtins.property
    def force_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When deleting a bucket, this boolean option will delete all contained objects, or anywhereCaches (if any).

        If you try to delete a bucket that contains objects or anywhereCaches, Terraform will fail that run, deleting anywhereCaches may take 80 minutes to complete.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#force_destroy GoogleStorageBucket#force_destroy}
        '''
        result = self._values.get("force_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hierarchical_namespace(
        self,
    ) -> typing.Optional["GoogleStorageBucketHierarchicalNamespace"]:
        '''hierarchical_namespace block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#hierarchical_namespace GoogleStorageBucket#hierarchical_namespace}
        '''
        result = self._values.get("hierarchical_namespace")
        return typing.cast(typing.Optional["GoogleStorageBucketHierarchicalNamespace"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#id GoogleStorageBucket#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_filter(self) -> typing.Optional["GoogleStorageBucketIpFilter"]:
        '''ip_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#ip_filter GoogleStorageBucket#ip_filter}
        '''
        result = self._values.get("ip_filter")
        return typing.cast(typing.Optional["GoogleStorageBucketIpFilter"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#labels GoogleStorageBucket#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def lifecycle_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageBucketLifecycleRule"]]]:
        '''lifecycle_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#lifecycle_rule GoogleStorageBucket#lifecycle_rule}
        '''
        result = self._values.get("lifecycle_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageBucketLifecycleRule"]]], result)

    @builtins.property
    def logging(self) -> typing.Optional["GoogleStorageBucketLogging"]:
        '''logging block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#logging GoogleStorageBucket#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional["GoogleStorageBucketLogging"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#project GoogleStorageBucket#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_access_prevention(self) -> typing.Optional[builtins.str]:
        '''Prevents public access to a bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#public_access_prevention GoogleStorageBucket#public_access_prevention}
        '''
        result = self._values.get("public_access_prevention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requester_pays(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Requester Pays on a storage bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#requester_pays GoogleStorageBucket#requester_pays}
        '''
        result = self._values.get("requester_pays")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retention_policy(self) -> typing.Optional["GoogleStorageBucketRetentionPolicy"]:
        '''retention_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#retention_policy GoogleStorageBucket#retention_policy}
        '''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional["GoogleStorageBucketRetentionPolicy"], result)

    @builtins.property
    def rpo(self) -> typing.Optional[builtins.str]:
        '''Specifies the RPO setting of bucket.

        If set 'ASYNC_TURBO', The Turbo Replication will be enabled for the dual-region bucket. Value 'DEFAULT' will set RPO setting to default. Turbo Replication is only for buckets in dual-regions.See the docs for more details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#rpo GoogleStorageBucket#rpo}
        '''
        result = self._values.get("rpo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def soft_delete_policy(
        self,
    ) -> typing.Optional["GoogleStorageBucketSoftDeletePolicy"]:
        '''soft_delete_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#soft_delete_policy GoogleStorageBucket#soft_delete_policy}
        '''
        result = self._values.get("soft_delete_policy")
        return typing.cast(typing.Optional["GoogleStorageBucketSoftDeletePolicy"], result)

    @builtins.property
    def storage_class(self) -> typing.Optional[builtins.str]:
        '''The Storage Class of the new bucket. Supported values include: STANDARD, MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#storage_class GoogleStorageBucket#storage_class}
        '''
        result = self._values.get("storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleStorageBucketTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#timeouts GoogleStorageBucket#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleStorageBucketTimeouts"], result)

    @builtins.property
    def uniform_bucket_level_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables uniform bucket-level access on a bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#uniform_bucket_level_access GoogleStorageBucket#uniform_bucket_level_access}
        '''
        result = self._values.get("uniform_bucket_level_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def versioning(self) -> typing.Optional["GoogleStorageBucketVersioning"]:
        '''versioning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#versioning GoogleStorageBucket#versioning}
        '''
        result = self._values.get("versioning")
        return typing.cast(typing.Optional["GoogleStorageBucketVersioning"], result)

    @builtins.property
    def website(self) -> typing.Optional["GoogleStorageBucketWebsite"]:
        '''website block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#website GoogleStorageBucket#website}
        '''
        result = self._values.get("website")
        return typing.cast(typing.Optional["GoogleStorageBucketWebsite"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketCors",
    jsii_struct_bases=[],
    name_mapping={
        "max_age_seconds": "maxAgeSeconds",
        "method": "method",
        "origin": "origin",
        "response_header": "responseHeader",
    },
)
class GoogleStorageBucketCors:
    def __init__(
        self,
        *,
        max_age_seconds: typing.Optional[jsii.Number] = None,
        method: typing.Optional[typing.Sequence[builtins.str]] = None,
        origin: typing.Optional[typing.Sequence[builtins.str]] = None,
        response_header: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param max_age_seconds: The value, in seconds, to return in the Access-Control-Max-Age header used in preflight responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#max_age_seconds GoogleStorageBucket#max_age_seconds}
        :param method: The list of HTTP methods on which to include CORS response headers, (GET, OPTIONS, POST, etc) Note: "*" is permitted in the list of methods, and means "any method". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#method GoogleStorageBucket#method}
        :param origin: The list of Origins eligible to receive CORS response headers. Note: "*" is permitted in the list of origins, and means "any Origin". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#origin GoogleStorageBucket#origin}
        :param response_header: The list of HTTP headers other than the simple response headers to give permission for the user-agent to share across domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#response_header GoogleStorageBucket#response_header}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54cc81faf65f2ea3a53c738ac18d03e6dbd526761949c092e21a57efc0ebc5b2)
            check_type(argname="argument max_age_seconds", value=max_age_seconds, expected_type=type_hints["max_age_seconds"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            check_type(argname="argument response_header", value=response_header, expected_type=type_hints["response_header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_age_seconds is not None:
            self._values["max_age_seconds"] = max_age_seconds
        if method is not None:
            self._values["method"] = method
        if origin is not None:
            self._values["origin"] = origin
        if response_header is not None:
            self._values["response_header"] = response_header

    @builtins.property
    def max_age_seconds(self) -> typing.Optional[jsii.Number]:
        '''The value, in seconds, to return in the Access-Control-Max-Age header used in preflight responses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#max_age_seconds GoogleStorageBucket#max_age_seconds}
        '''
        result = self._values.get("max_age_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def method(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of HTTP methods on which to include CORS response headers, (GET, OPTIONS, POST, etc) Note: "*" is permitted in the list of methods, and means "any method".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#method GoogleStorageBucket#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def origin(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of Origins eligible to receive CORS response headers.

        Note: "*" is permitted in the list of origins, and means "any Origin".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#origin GoogleStorageBucket#origin}
        '''
        result = self._values.get("origin")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def response_header(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of HTTP headers other than the simple response headers to give permission for the user-agent to share across domains.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#response_header GoogleStorageBucket#response_header}
        '''
        result = self._values.get("response_header")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketCors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketCorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketCorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29d650083baecfe4ce34c1a39ec4eff283dbd0b2d6b47d4ad5c3b45f2e75cfa5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GoogleStorageBucketCorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e773c059aef636a85ab61356e37afb680dacec910241876b5ddb7388e7afa06)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleStorageBucketCorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eeae2b6eaf08292574fe559c1eeedc7f74dfa21b3c2b061ee7e3bf4af821416)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9bef737a34de97248a8959020056ade164453f39cd4357f76009ca22df5acbb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b626fec4d1c9251a4594f63cb583205110d50cb55fe4c0507506603350fa21f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageBucketCors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageBucketCors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageBucketCors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d7ac1cb1cad9ed3382bf17d9d6b4d53172274dd1ca19832662a4a6c18e0f32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleStorageBucketCorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketCorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d9a24725956a2509162eaf45e98ec7297c791533c7b4a4b0aead881c4547b0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMaxAgeSeconds")
    def reset_max_age_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAgeSeconds", []))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetOrigin")
    def reset_origin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrigin", []))

    @jsii.member(jsii_name="resetResponseHeader")
    def reset_response_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseHeader", []))

    @builtins.property
    @jsii.member(jsii_name="maxAgeSecondsInput")
    def max_age_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAgeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="originInput")
    def origin_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "originInput"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderInput")
    def response_header_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "responseHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeSeconds")
    def max_age_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAgeSeconds"))

    @max_age_seconds.setter
    def max_age_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c89bcae2dc30121dbe0a5bf049a3ffe239e12f218039c2e62100fd04dfa8303f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAgeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "method"))

    @method.setter
    def method(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e08391c96391e72c5a919163d7db239873546bff1a8d599f94bbc10db908e64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="origin")
    def origin(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "origin"))

    @origin.setter
    def origin(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66c52c6dc8b9a0193d2f1fab192bfb83c963b9bd7131666b898423e22aab23a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "origin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseHeader")
    def response_header(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "responseHeader"))

    @response_header.setter
    def response_header(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9a3404ac321e63c9f0fff6249ff4180a7fec01f805df1791aed40b56adcdb6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketCors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketCors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketCors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa6dc66e9f5d25c553465713e04e0f59be329693430e5773d155811b9836244)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketCustomPlacementConfig",
    jsii_struct_bases=[],
    name_mapping={"data_locations": "dataLocations"},
)
class GoogleStorageBucketCustomPlacementConfig:
    def __init__(self, *, data_locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param data_locations: The list of individual regions that comprise a dual-region bucket. See the docs for a list of acceptable regions. Note: If any of the data_locations changes, it will recreate the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#data_locations GoogleStorageBucket#data_locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3505625673f21db4874ba0436a05b091f1597e94ffc3181d927a9fb83357b84)
            check_type(argname="argument data_locations", value=data_locations, expected_type=type_hints["data_locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_locations": data_locations,
        }

    @builtins.property
    def data_locations(self) -> typing.List[builtins.str]:
        '''The list of individual regions that comprise a dual-region bucket.

        See the docs for a list of acceptable regions. Note: If any of the data_locations changes, it will recreate the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#data_locations GoogleStorageBucket#data_locations}
        '''
        result = self._values.get("data_locations")
        assert result is not None, "Required property 'data_locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketCustomPlacementConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketCustomPlacementConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketCustomPlacementConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80c3c75aee6b8d81806dcbd0730c18a21a1b7aa6a8bcf32b224bafa695ecd285)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dataLocationsInput")
    def data_locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dataLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataLocations")
    def data_locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dataLocations"))

    @data_locations.setter
    def data_locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8ef5b9f3d596ec9c8fa718cb048fffbbdcc5ba5c53fe4e57e7547e85b43dd08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataLocations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageBucketCustomPlacementConfig]:
        return typing.cast(typing.Optional[GoogleStorageBucketCustomPlacementConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBucketCustomPlacementConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0a67149444e2556c43af5559d72a90856f1cdf204653b76dc648efc31e611a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketEncryption",
    jsii_struct_bases=[],
    name_mapping={"default_kms_key_name": "defaultKmsKeyName"},
)
class GoogleStorageBucketEncryption:
    def __init__(self, *, default_kms_key_name: builtins.str) -> None:
        '''
        :param default_kms_key_name: A Cloud KMS key that will be used to encrypt objects inserted into this bucket, if no encryption method is specified. You must pay attention to whether the crypto key is available in the location that this bucket is created in. See the docs for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#default_kms_key_name GoogleStorageBucket#default_kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4afb464e305051d9ee9b623daa22e6bd68ea76688ee9ac878dfc932742862a16)
            check_type(argname="argument default_kms_key_name", value=default_kms_key_name, expected_type=type_hints["default_kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_kms_key_name": default_kms_key_name,
        }

    @builtins.property
    def default_kms_key_name(self) -> builtins.str:
        '''A Cloud KMS key that will be used to encrypt objects inserted into this bucket, if no encryption method is specified.

        You must pay attention to whether the crypto key is available in the location that this bucket is created in. See the docs for more details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#default_kms_key_name GoogleStorageBucket#default_kms_key_name}
        '''
        result = self._values.get("default_kms_key_name")
        assert result is not None, "Required property 'default_kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__155b617c67cc1eae002aaf18e88814036514deb39cfb18b7aa4c7ef15d111a59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="defaultKmsKeyNameInput")
    def default_kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultKmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultKmsKeyName")
    def default_kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultKmsKeyName"))

    @default_kms_key_name.setter
    def default_kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032c68510a5048508ea0028f88fc09719c1eea051de66c0aeaf837b70ca8edbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultKmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleStorageBucketEncryption]:
        return typing.cast(typing.Optional[GoogleStorageBucketEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBucketEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a8f0d5fc564596d46016fb74324d0bdbd1e79a129a9aac413e20c065c78d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketHierarchicalNamespace",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleStorageBucketHierarchicalNamespace:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Set this field true to organize bucket with logical file system structure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#enabled GoogleStorageBucket#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394d06d860fd468468bbc838904a1682b88959b92ca5d21ca6d2c1f8f3a7e460)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Set this field true to organize bucket with logical file system structure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#enabled GoogleStorageBucket#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketHierarchicalNamespace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketHierarchicalNamespaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketHierarchicalNamespaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96e709e90fac1459f2c333b63a80b1f57e41d043663e8d3cf1668f9d19da370a)
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
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a491432a96a870691334a65746297b8f8d278157e1e84e00de4a5a57b9928679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageBucketHierarchicalNamespace]:
        return typing.cast(typing.Optional[GoogleStorageBucketHierarchicalNamespace], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBucketHierarchicalNamespace],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f7f56df3c15ee4746f692e73724cdb98f784571c3ed17cda9d4f85d208ad5d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketIpFilter",
    jsii_struct_bases=[],
    name_mapping={
        "mode": "mode",
        "public_network_source": "publicNetworkSource",
        "vpc_network_sources": "vpcNetworkSources",
    },
)
class GoogleStorageBucketIpFilter:
    def __init__(
        self,
        *,
        mode: builtins.str,
        public_network_source: typing.Optional[typing.Union["GoogleStorageBucketIpFilterPublicNetworkSource", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_network_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleStorageBucketIpFilterVpcNetworkSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param mode: The mode of the IP filter. Valid values are 'Enabled' and 'Disabled'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#mode GoogleStorageBucket#mode}
        :param public_network_source: public_network_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#public_network_source GoogleStorageBucket#public_network_source}
        :param vpc_network_sources: vpc_network_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#vpc_network_sources GoogleStorageBucket#vpc_network_sources}
        '''
        if isinstance(public_network_source, dict):
            public_network_source = GoogleStorageBucketIpFilterPublicNetworkSource(**public_network_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40da5b3d77655a384e56f9dc4044d4770d4398dadf61f93098e5ab6c279cdc8e)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument public_network_source", value=public_network_source, expected_type=type_hints["public_network_source"])
            check_type(argname="argument vpc_network_sources", value=vpc_network_sources, expected_type=type_hints["vpc_network_sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if public_network_source is not None:
            self._values["public_network_source"] = public_network_source
        if vpc_network_sources is not None:
            self._values["vpc_network_sources"] = vpc_network_sources

    @builtins.property
    def mode(self) -> builtins.str:
        '''The mode of the IP filter. Valid values are 'Enabled' and 'Disabled'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#mode GoogleStorageBucket#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def public_network_source(
        self,
    ) -> typing.Optional["GoogleStorageBucketIpFilterPublicNetworkSource"]:
        '''public_network_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#public_network_source GoogleStorageBucket#public_network_source}
        '''
        result = self._values.get("public_network_source")
        return typing.cast(typing.Optional["GoogleStorageBucketIpFilterPublicNetworkSource"], result)

    @builtins.property
    def vpc_network_sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageBucketIpFilterVpcNetworkSources"]]]:
        '''vpc_network_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#vpc_network_sources GoogleStorageBucket#vpc_network_sources}
        '''
        result = self._values.get("vpc_network_sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageBucketIpFilterVpcNetworkSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketIpFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketIpFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketIpFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__991138c050c70ddefa91b6ffd902812515ad56bdba8e6d1e2de61135d64e4725)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPublicNetworkSource")
    def put_public_network_source(
        self,
        *,
        allowed_ip_cidr_ranges: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param allowed_ip_cidr_ranges: The list of public IPv4, IPv6 cidr ranges that are allowed to access the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#allowed_ip_cidr_ranges GoogleStorageBucket#allowed_ip_cidr_ranges}
        '''
        value = GoogleStorageBucketIpFilterPublicNetworkSource(
            allowed_ip_cidr_ranges=allowed_ip_cidr_ranges
        )

        return typing.cast(None, jsii.invoke(self, "putPublicNetworkSource", [value]))

    @jsii.member(jsii_name="putVpcNetworkSources")
    def put_vpc_network_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleStorageBucketIpFilterVpcNetworkSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9786742d92b3b598596679d732da484e0f2df2f86c4f00c9f62263bb4492d9eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVpcNetworkSources", [value]))

    @jsii.member(jsii_name="resetPublicNetworkSource")
    def reset_public_network_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkSource", []))

    @jsii.member(jsii_name="resetVpcNetworkSources")
    def reset_vpc_network_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcNetworkSources", []))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkSource")
    def public_network_source(
        self,
    ) -> "GoogleStorageBucketIpFilterPublicNetworkSourceOutputReference":
        return typing.cast("GoogleStorageBucketIpFilterPublicNetworkSourceOutputReference", jsii.get(self, "publicNetworkSource"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetworkSources")
    def vpc_network_sources(self) -> "GoogleStorageBucketIpFilterVpcNetworkSourcesList":
        return typing.cast("GoogleStorageBucketIpFilterVpcNetworkSourcesList", jsii.get(self, "vpcNetworkSources"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkSourceInput")
    def public_network_source_input(
        self,
    ) -> typing.Optional["GoogleStorageBucketIpFilterPublicNetworkSource"]:
        return typing.cast(typing.Optional["GoogleStorageBucketIpFilterPublicNetworkSource"], jsii.get(self, "publicNetworkSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetworkSourcesInput")
    def vpc_network_sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageBucketIpFilterVpcNetworkSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleStorageBucketIpFilterVpcNetworkSources"]]], jsii.get(self, "vpcNetworkSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7fe79326f1243c9ca974331cea65663b011335ab175ff04bebc951c2d52e4e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleStorageBucketIpFilter]:
        return typing.cast(typing.Optional[GoogleStorageBucketIpFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBucketIpFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__272f4997866ca483499993c2f355b61f04f26196b2eb5c9c43d0a6f5cae3e525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketIpFilterPublicNetworkSource",
    jsii_struct_bases=[],
    name_mapping={"allowed_ip_cidr_ranges": "allowedIpCidrRanges"},
)
class GoogleStorageBucketIpFilterPublicNetworkSource:
    def __init__(
        self,
        *,
        allowed_ip_cidr_ranges: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param allowed_ip_cidr_ranges: The list of public IPv4, IPv6 cidr ranges that are allowed to access the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#allowed_ip_cidr_ranges GoogleStorageBucket#allowed_ip_cidr_ranges}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9afeafc87bc7c63c72f37b0391aee1b9835287c959f366f33f18bdab7cd882ea)
            check_type(argname="argument allowed_ip_cidr_ranges", value=allowed_ip_cidr_ranges, expected_type=type_hints["allowed_ip_cidr_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_ip_cidr_ranges": allowed_ip_cidr_ranges,
        }

    @builtins.property
    def allowed_ip_cidr_ranges(self) -> typing.List[builtins.str]:
        '''The list of public IPv4, IPv6 cidr ranges that are allowed to access the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#allowed_ip_cidr_ranges GoogleStorageBucket#allowed_ip_cidr_ranges}
        '''
        result = self._values.get("allowed_ip_cidr_ranges")
        assert result is not None, "Required property 'allowed_ip_cidr_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketIpFilterPublicNetworkSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketIpFilterPublicNetworkSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketIpFilterPublicNetworkSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__740b4aeb4584b29ded363eef0fca16d893b38007e9af3848653760d78e29762a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="allowedIpCidrRangesInput")
    def allowed_ip_cidr_ranges_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedIpCidrRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedIpCidrRanges")
    def allowed_ip_cidr_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedIpCidrRanges"))

    @allowed_ip_cidr_ranges.setter
    def allowed_ip_cidr_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd7228308ccabaae57845ddd25dec366f42de630b6bfec48a29a08020af9e3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedIpCidrRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageBucketIpFilterPublicNetworkSource]:
        return typing.cast(typing.Optional[GoogleStorageBucketIpFilterPublicNetworkSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBucketIpFilterPublicNetworkSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a918474a8d141269a52177610c18729a2c7c6a92e652af41d89049cd493d0718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketIpFilterVpcNetworkSources",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_ip_cidr_ranges": "allowedIpCidrRanges",
        "network": "network",
    },
)
class GoogleStorageBucketIpFilterVpcNetworkSources:
    def __init__(
        self,
        *,
        allowed_ip_cidr_ranges: typing.Sequence[builtins.str],
        network: builtins.str,
    ) -> None:
        '''
        :param allowed_ip_cidr_ranges: The list of public or private IPv4 and IPv6 CIDR ranges that can access the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#allowed_ip_cidr_ranges GoogleStorageBucket#allowed_ip_cidr_ranges}
        :param network: Name of the network. Format: projects/{PROJECT_ID}/global/networks/{NETWORK_NAME}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#network GoogleStorageBucket#network}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b97b37f6b247df9e8407bb807fc87c005d60528ea6980881fdf1db2b5db8a5)
            check_type(argname="argument allowed_ip_cidr_ranges", value=allowed_ip_cidr_ranges, expected_type=type_hints["allowed_ip_cidr_ranges"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_ip_cidr_ranges": allowed_ip_cidr_ranges,
            "network": network,
        }

    @builtins.property
    def allowed_ip_cidr_ranges(self) -> typing.List[builtins.str]:
        '''The list of public or private IPv4 and IPv6 CIDR ranges that can access the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#allowed_ip_cidr_ranges GoogleStorageBucket#allowed_ip_cidr_ranges}
        '''
        result = self._values.get("allowed_ip_cidr_ranges")
        assert result is not None, "Required property 'allowed_ip_cidr_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def network(self) -> builtins.str:
        '''Name of the network. Format: projects/{PROJECT_ID}/global/networks/{NETWORK_NAME}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#network GoogleStorageBucket#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketIpFilterVpcNetworkSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketIpFilterVpcNetworkSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketIpFilterVpcNetworkSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5808e359de6d3ea9480b9127e16d7e98a79c4151317861f829665b261e695de9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleStorageBucketIpFilterVpcNetworkSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c5ad6137b1ec722b9b735451db7e4748e73db74114933659261f756363e73e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleStorageBucketIpFilterVpcNetworkSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ec7250857ad9937ec3c21c96c384ff483900accda7241d00d32c653f99779fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcf36f0c3ebe78a05b484ca97d0c0fadecce1368cb1f4a7f321ba2631722ba50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e79cfdcc12557fc894d04fab4fc516ad018e1e73048dea787e9f86b225a249b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageBucketIpFilterVpcNetworkSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageBucketIpFilterVpcNetworkSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageBucketIpFilterVpcNetworkSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__769cecfa807df146ef8b637edc0511b65a5441ba8a06eea22c51f7add540b8c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleStorageBucketIpFilterVpcNetworkSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketIpFilterVpcNetworkSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75843a1b4d6c3b9d504e923e4440a283529e04edad810cac95234e1227df88fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowedIpCidrRangesInput")
    def allowed_ip_cidr_ranges_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedIpCidrRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedIpCidrRanges")
    def allowed_ip_cidr_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedIpCidrRanges"))

    @allowed_ip_cidr_ranges.setter
    def allowed_ip_cidr_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33fd38c970f7e56eeaed5cfbcfa75760361f5e57392fa1c3d3af544b2424936e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedIpCidrRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c3e22755a4bae2d0b5ce98c498291f2db7732d4cfb3dc076395b7dde97a161a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketIpFilterVpcNetworkSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketIpFilterVpcNetworkSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketIpFilterVpcNetworkSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e0142e1dfdf35768ab177489662aed5fc0a5ae17053550c82c84138b6cc065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketLifecycleRule",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "condition": "condition"},
)
class GoogleStorageBucketLifecycleRule:
    def __init__(
        self,
        *,
        action: typing.Union["GoogleStorageBucketLifecycleRuleAction", typing.Dict[builtins.str, typing.Any]],
        condition: typing.Union["GoogleStorageBucketLifecycleRuleCondition", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#action GoogleStorageBucket#action}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#condition GoogleStorageBucket#condition}
        '''
        if isinstance(action, dict):
            action = GoogleStorageBucketLifecycleRuleAction(**action)
        if isinstance(condition, dict):
            condition = GoogleStorageBucketLifecycleRuleCondition(**condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd8d36e84494c14e7380db271694c87dacbe1c2e103075ca47494ebf50d88ed8)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "condition": condition,
        }

    @builtins.property
    def action(self) -> "GoogleStorageBucketLifecycleRuleAction":
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#action GoogleStorageBucket#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("GoogleStorageBucketLifecycleRuleAction", result)

    @builtins.property
    def condition(self) -> "GoogleStorageBucketLifecycleRuleCondition":
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#condition GoogleStorageBucket#condition}
        '''
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast("GoogleStorageBucketLifecycleRuleCondition", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketLifecycleRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketLifecycleRuleAction",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "storage_class": "storageClass"},
)
class GoogleStorageBucketLifecycleRuleAction:
    def __init__(
        self,
        *,
        type: builtins.str,
        storage_class: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: The type of the action of this Lifecycle Rule. Supported values include: Delete, SetStorageClass and AbortIncompleteMultipartUpload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#type GoogleStorageBucket#type}
        :param storage_class: The target Storage Class of objects affected by this Lifecycle Rule. Supported values include: MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#storage_class GoogleStorageBucket#storage_class}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b3ac7d760d045f0448d968562b532414e1d4a60964aaa8c857ee09e42f06dc)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if storage_class is not None:
            self._values["storage_class"] = storage_class

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the action of this Lifecycle Rule. Supported values include: Delete, SetStorageClass and AbortIncompleteMultipartUpload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#type GoogleStorageBucket#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_class(self) -> typing.Optional[builtins.str]:
        '''The target Storage Class of objects affected by this Lifecycle Rule. Supported values include: MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#storage_class GoogleStorageBucket#storage_class}
        '''
        result = self._values.get("storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketLifecycleRuleAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketLifecycleRuleActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketLifecycleRuleActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccdf950211915ad9a10cd42f5b5e04705bd2115603001951c58032eab163f735)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStorageClass")
    def reset_storage_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageClass", []))

    @builtins.property
    @jsii.member(jsii_name="storageClassInput")
    def storage_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50db44fc996b8b85559a846d29b9e2a9826ed25eb4fe0d8eec70ddfbc0ab873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2defb3cdc3f0e3e06a8a4643bb9a49553c8459c3436d0bf559f2d36b26660572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleStorageBucketLifecycleRuleAction]:
        return typing.cast(typing.Optional[GoogleStorageBucketLifecycleRuleAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBucketLifecycleRuleAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03bd90466ae7033d71d27730e045147739fd5344602c003609f177f545fd63ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketLifecycleRuleCondition",
    jsii_struct_bases=[],
    name_mapping={
        "age": "age",
        "created_before": "createdBefore",
        "custom_time_before": "customTimeBefore",
        "days_since_custom_time": "daysSinceCustomTime",
        "days_since_noncurrent_time": "daysSinceNoncurrentTime",
        "matches_prefix": "matchesPrefix",
        "matches_storage_class": "matchesStorageClass",
        "matches_suffix": "matchesSuffix",
        "noncurrent_time_before": "noncurrentTimeBefore",
        "num_newer_versions": "numNewerVersions",
        "send_age_if_zero": "sendAgeIfZero",
        "send_days_since_custom_time_if_zero": "sendDaysSinceCustomTimeIfZero",
        "send_days_since_noncurrent_time_if_zero": "sendDaysSinceNoncurrentTimeIfZero",
        "send_num_newer_versions_if_zero": "sendNumNewerVersionsIfZero",
        "with_state": "withState",
    },
)
class GoogleStorageBucketLifecycleRuleCondition:
    def __init__(
        self,
        *,
        age: typing.Optional[jsii.Number] = None,
        created_before: typing.Optional[builtins.str] = None,
        custom_time_before: typing.Optional[builtins.str] = None,
        days_since_custom_time: typing.Optional[jsii.Number] = None,
        days_since_noncurrent_time: typing.Optional[jsii.Number] = None,
        matches_prefix: typing.Optional[typing.Sequence[builtins.str]] = None,
        matches_storage_class: typing.Optional[typing.Sequence[builtins.str]] = None,
        matches_suffix: typing.Optional[typing.Sequence[builtins.str]] = None,
        noncurrent_time_before: typing.Optional[builtins.str] = None,
        num_newer_versions: typing.Optional[jsii.Number] = None,
        send_age_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_days_since_custom_time_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_days_since_noncurrent_time_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_num_newer_versions_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        with_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param age: Minimum age of an object in days to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#age GoogleStorageBucket#age}
        :param created_before: Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#created_before GoogleStorageBucket#created_before}
        :param custom_time_before: Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#custom_time_before GoogleStorageBucket#custom_time_before}
        :param days_since_custom_time: Number of days elapsed since the user-specified timestamp set on an object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#days_since_custom_time GoogleStorageBucket#days_since_custom_time}
        :param days_since_noncurrent_time: Number of days elapsed since the noncurrent timestamp of an object. This condition is relevant only for versioned objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#days_since_noncurrent_time GoogleStorageBucket#days_since_noncurrent_time}
        :param matches_prefix: One or more matching name prefixes to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#matches_prefix GoogleStorageBucket#matches_prefix}
        :param matches_storage_class: Storage Class of objects to satisfy this condition. Supported values include: MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE, STANDARD, DURABLE_REDUCED_AVAILABILITY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#matches_storage_class GoogleStorageBucket#matches_storage_class}
        :param matches_suffix: One or more matching name suffixes to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#matches_suffix GoogleStorageBucket#matches_suffix}
        :param noncurrent_time_before: Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#noncurrent_time_before GoogleStorageBucket#noncurrent_time_before}
        :param num_newer_versions: Relevant only for versioned objects. The number of newer versions of an object to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#num_newer_versions GoogleStorageBucket#num_newer_versions}
        :param send_age_if_zero: While set true, age value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the age field. It can be used alone or together with age. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#send_age_if_zero GoogleStorageBucket#send_age_if_zero}
        :param send_days_since_custom_time_if_zero: While set true, days_since_custom_time value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the days_since_custom_time field. It can be used alone or together with days_since_custom_time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#send_days_since_custom_time_if_zero GoogleStorageBucket#send_days_since_custom_time_if_zero}
        :param send_days_since_noncurrent_time_if_zero: While set true, days_since_noncurrent_time value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the days_since_noncurrent_time field. It can be used alone or together with days_since_noncurrent_time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#send_days_since_noncurrent_time_if_zero GoogleStorageBucket#send_days_since_noncurrent_time_if_zero}
        :param send_num_newer_versions_if_zero: While set true, num_newer_versions value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the num_newer_versions field. It can be used alone or together with num_newer_versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#send_num_newer_versions_if_zero GoogleStorageBucket#send_num_newer_versions_if_zero}
        :param with_state: Match to live and/or archived objects. Unversioned buckets have only live objects. Supported values include: "LIVE", "ARCHIVED", "ANY". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#with_state GoogleStorageBucket#with_state}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10bfb170d9bff6a49b44134faf5b950d91e1a3958f05ecf519f2fd153f633be8)
            check_type(argname="argument age", value=age, expected_type=type_hints["age"])
            check_type(argname="argument created_before", value=created_before, expected_type=type_hints["created_before"])
            check_type(argname="argument custom_time_before", value=custom_time_before, expected_type=type_hints["custom_time_before"])
            check_type(argname="argument days_since_custom_time", value=days_since_custom_time, expected_type=type_hints["days_since_custom_time"])
            check_type(argname="argument days_since_noncurrent_time", value=days_since_noncurrent_time, expected_type=type_hints["days_since_noncurrent_time"])
            check_type(argname="argument matches_prefix", value=matches_prefix, expected_type=type_hints["matches_prefix"])
            check_type(argname="argument matches_storage_class", value=matches_storage_class, expected_type=type_hints["matches_storage_class"])
            check_type(argname="argument matches_suffix", value=matches_suffix, expected_type=type_hints["matches_suffix"])
            check_type(argname="argument noncurrent_time_before", value=noncurrent_time_before, expected_type=type_hints["noncurrent_time_before"])
            check_type(argname="argument num_newer_versions", value=num_newer_versions, expected_type=type_hints["num_newer_versions"])
            check_type(argname="argument send_age_if_zero", value=send_age_if_zero, expected_type=type_hints["send_age_if_zero"])
            check_type(argname="argument send_days_since_custom_time_if_zero", value=send_days_since_custom_time_if_zero, expected_type=type_hints["send_days_since_custom_time_if_zero"])
            check_type(argname="argument send_days_since_noncurrent_time_if_zero", value=send_days_since_noncurrent_time_if_zero, expected_type=type_hints["send_days_since_noncurrent_time_if_zero"])
            check_type(argname="argument send_num_newer_versions_if_zero", value=send_num_newer_versions_if_zero, expected_type=type_hints["send_num_newer_versions_if_zero"])
            check_type(argname="argument with_state", value=with_state, expected_type=type_hints["with_state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if age is not None:
            self._values["age"] = age
        if created_before is not None:
            self._values["created_before"] = created_before
        if custom_time_before is not None:
            self._values["custom_time_before"] = custom_time_before
        if days_since_custom_time is not None:
            self._values["days_since_custom_time"] = days_since_custom_time
        if days_since_noncurrent_time is not None:
            self._values["days_since_noncurrent_time"] = days_since_noncurrent_time
        if matches_prefix is not None:
            self._values["matches_prefix"] = matches_prefix
        if matches_storage_class is not None:
            self._values["matches_storage_class"] = matches_storage_class
        if matches_suffix is not None:
            self._values["matches_suffix"] = matches_suffix
        if noncurrent_time_before is not None:
            self._values["noncurrent_time_before"] = noncurrent_time_before
        if num_newer_versions is not None:
            self._values["num_newer_versions"] = num_newer_versions
        if send_age_if_zero is not None:
            self._values["send_age_if_zero"] = send_age_if_zero
        if send_days_since_custom_time_if_zero is not None:
            self._values["send_days_since_custom_time_if_zero"] = send_days_since_custom_time_if_zero
        if send_days_since_noncurrent_time_if_zero is not None:
            self._values["send_days_since_noncurrent_time_if_zero"] = send_days_since_noncurrent_time_if_zero
        if send_num_newer_versions_if_zero is not None:
            self._values["send_num_newer_versions_if_zero"] = send_num_newer_versions_if_zero
        if with_state is not None:
            self._values["with_state"] = with_state

    @builtins.property
    def age(self) -> typing.Optional[jsii.Number]:
        '''Minimum age of an object in days to satisfy this condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#age GoogleStorageBucket#age}
        '''
        result = self._values.get("age")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def created_before(self) -> typing.Optional[builtins.str]:
        '''Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#created_before GoogleStorageBucket#created_before}
        '''
        result = self._values.get("created_before")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_time_before(self) -> typing.Optional[builtins.str]:
        '''Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#custom_time_before GoogleStorageBucket#custom_time_before}
        '''
        result = self._values.get("custom_time_before")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def days_since_custom_time(self) -> typing.Optional[jsii.Number]:
        '''Number of days elapsed since the user-specified timestamp set on an object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#days_since_custom_time GoogleStorageBucket#days_since_custom_time}
        '''
        result = self._values.get("days_since_custom_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def days_since_noncurrent_time(self) -> typing.Optional[jsii.Number]:
        '''Number of days elapsed since the noncurrent timestamp of an object. This 										condition is relevant only for versioned objects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#days_since_noncurrent_time GoogleStorageBucket#days_since_noncurrent_time}
        '''
        result = self._values.get("days_since_noncurrent_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def matches_prefix(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more matching name prefixes to satisfy this condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#matches_prefix GoogleStorageBucket#matches_prefix}
        '''
        result = self._values.get("matches_prefix")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def matches_storage_class(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Storage Class of objects to satisfy this condition. Supported values include: MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE, STANDARD, DURABLE_REDUCED_AVAILABILITY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#matches_storage_class GoogleStorageBucket#matches_storage_class}
        '''
        result = self._values.get("matches_storage_class")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def matches_suffix(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more matching name suffixes to satisfy this condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#matches_suffix GoogleStorageBucket#matches_suffix}
        '''
        result = self._values.get("matches_suffix")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def noncurrent_time_before(self) -> typing.Optional[builtins.str]:
        '''Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#noncurrent_time_before GoogleStorageBucket#noncurrent_time_before}
        '''
        result = self._values.get("noncurrent_time_before")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_newer_versions(self) -> typing.Optional[jsii.Number]:
        '''Relevant only for versioned objects. The number of newer versions of an object to satisfy this condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#num_newer_versions GoogleStorageBucket#num_newer_versions}
        '''
        result = self._values.get("num_newer_versions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def send_age_if_zero(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''While set true, age value will be sent in the request even for zero value of the field.

        This field is only useful for setting 0 value to the age field. It can be used alone or together with age.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#send_age_if_zero GoogleStorageBucket#send_age_if_zero}
        '''
        result = self._values.get("send_age_if_zero")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_days_since_custom_time_if_zero(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''While set true, days_since_custom_time value will be sent in the request even for zero value of the field.

        This field is only useful for setting 0 value to the days_since_custom_time field. It can be used alone or together with days_since_custom_time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#send_days_since_custom_time_if_zero GoogleStorageBucket#send_days_since_custom_time_if_zero}
        '''
        result = self._values.get("send_days_since_custom_time_if_zero")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_days_since_noncurrent_time_if_zero(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''While set true, days_since_noncurrent_time value will be sent in the request even for zero value of the field.

        This field is only useful for setting 0 value to the days_since_noncurrent_time field. It can be used alone or together with days_since_noncurrent_time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#send_days_since_noncurrent_time_if_zero GoogleStorageBucket#send_days_since_noncurrent_time_if_zero}
        '''
        result = self._values.get("send_days_since_noncurrent_time_if_zero")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_num_newer_versions_if_zero(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''While set true, num_newer_versions value will be sent in the request even for zero value of the field.

        This field is only useful for setting 0 value to the num_newer_versions field. It can be used alone or together with num_newer_versions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#send_num_newer_versions_if_zero GoogleStorageBucket#send_num_newer_versions_if_zero}
        '''
        result = self._values.get("send_num_newer_versions_if_zero")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def with_state(self) -> typing.Optional[builtins.str]:
        '''Match to live and/or archived objects. Unversioned buckets have only live objects. Supported values include: "LIVE", "ARCHIVED", "ANY".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#with_state GoogleStorageBucket#with_state}
        '''
        result = self._values.get("with_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketLifecycleRuleCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketLifecycleRuleConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketLifecycleRuleConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91ebde1e1121464bd8c2a2fbc36b6edff413f4c1bda03936679437c31476b524)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAge")
    def reset_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAge", []))

    @jsii.member(jsii_name="resetCreatedBefore")
    def reset_created_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedBefore", []))

    @jsii.member(jsii_name="resetCustomTimeBefore")
    def reset_custom_time_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomTimeBefore", []))

    @jsii.member(jsii_name="resetDaysSinceCustomTime")
    def reset_days_since_custom_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysSinceCustomTime", []))

    @jsii.member(jsii_name="resetDaysSinceNoncurrentTime")
    def reset_days_since_noncurrent_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysSinceNoncurrentTime", []))

    @jsii.member(jsii_name="resetMatchesPrefix")
    def reset_matches_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchesPrefix", []))

    @jsii.member(jsii_name="resetMatchesStorageClass")
    def reset_matches_storage_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchesStorageClass", []))

    @jsii.member(jsii_name="resetMatchesSuffix")
    def reset_matches_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchesSuffix", []))

    @jsii.member(jsii_name="resetNoncurrentTimeBefore")
    def reset_noncurrent_time_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoncurrentTimeBefore", []))

    @jsii.member(jsii_name="resetNumNewerVersions")
    def reset_num_newer_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumNewerVersions", []))

    @jsii.member(jsii_name="resetSendAgeIfZero")
    def reset_send_age_if_zero(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendAgeIfZero", []))

    @jsii.member(jsii_name="resetSendDaysSinceCustomTimeIfZero")
    def reset_send_days_since_custom_time_if_zero(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendDaysSinceCustomTimeIfZero", []))

    @jsii.member(jsii_name="resetSendDaysSinceNoncurrentTimeIfZero")
    def reset_send_days_since_noncurrent_time_if_zero(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendDaysSinceNoncurrentTimeIfZero", []))

    @jsii.member(jsii_name="resetSendNumNewerVersionsIfZero")
    def reset_send_num_newer_versions_if_zero(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendNumNewerVersionsIfZero", []))

    @jsii.member(jsii_name="resetWithState")
    def reset_with_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithState", []))

    @builtins.property
    @jsii.member(jsii_name="ageInput")
    def age_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ageInput"))

    @builtins.property
    @jsii.member(jsii_name="createdBeforeInput")
    def created_before_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createdBeforeInput"))

    @builtins.property
    @jsii.member(jsii_name="customTimeBeforeInput")
    def custom_time_before_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customTimeBeforeInput"))

    @builtins.property
    @jsii.member(jsii_name="daysSinceCustomTimeInput")
    def days_since_custom_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysSinceCustomTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="daysSinceNoncurrentTimeInput")
    def days_since_noncurrent_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysSinceNoncurrentTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="matchesPrefixInput")
    def matches_prefix_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchesPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="matchesStorageClassInput")
    def matches_storage_class_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchesStorageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="matchesSuffixInput")
    def matches_suffix_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchesSuffixInput"))

    @builtins.property
    @jsii.member(jsii_name="noncurrentTimeBeforeInput")
    def noncurrent_time_before_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "noncurrentTimeBeforeInput"))

    @builtins.property
    @jsii.member(jsii_name="numNewerVersionsInput")
    def num_newer_versions_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numNewerVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sendAgeIfZeroInput")
    def send_age_if_zero_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendAgeIfZeroInput"))

    @builtins.property
    @jsii.member(jsii_name="sendDaysSinceCustomTimeIfZeroInput")
    def send_days_since_custom_time_if_zero_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendDaysSinceCustomTimeIfZeroInput"))

    @builtins.property
    @jsii.member(jsii_name="sendDaysSinceNoncurrentTimeIfZeroInput")
    def send_days_since_noncurrent_time_if_zero_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendDaysSinceNoncurrentTimeIfZeroInput"))

    @builtins.property
    @jsii.member(jsii_name="sendNumNewerVersionsIfZeroInput")
    def send_num_newer_versions_if_zero_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendNumNewerVersionsIfZeroInput"))

    @builtins.property
    @jsii.member(jsii_name="withStateInput")
    def with_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "withStateInput"))

    @builtins.property
    @jsii.member(jsii_name="age")
    def age(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "age"))

    @age.setter
    def age(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__726c5c4b3f115a675983875e43e10f3ee94719f2958f15e999151c599c559c75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "age", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createdBefore")
    def created_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdBefore"))

    @created_before.setter
    def created_before(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a92d0877fd3bc759e4f3163cb0f18530c5cd8767696f8c9ecf889c2e03eba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customTimeBefore")
    def custom_time_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customTimeBefore"))

    @custom_time_before.setter
    def custom_time_before(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__946beba83a867cc21efed880a1baf6b78dae8610da896b745120c54ac38d399e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customTimeBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="daysSinceCustomTime")
    def days_since_custom_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "daysSinceCustomTime"))

    @days_since_custom_time.setter
    def days_since_custom_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c89b9fde9a002fc8ea41f4757f5938e318409f9aab4bd54aa65fba47a6da18f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysSinceCustomTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="daysSinceNoncurrentTime")
    def days_since_noncurrent_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "daysSinceNoncurrentTime"))

    @days_since_noncurrent_time.setter
    def days_since_noncurrent_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b3c55dccfd288a6f7bee6d828d61569ca8d536b006477c17718fde12f85930f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysSinceNoncurrentTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchesPrefix")
    def matches_prefix(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchesPrefix"))

    @matches_prefix.setter
    def matches_prefix(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94db5fb467d1e4bee8db7f85e9927c544886d3d0dde960ef4276b2ea4a6b1d6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchesPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchesStorageClass")
    def matches_storage_class(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchesStorageClass"))

    @matches_storage_class.setter
    def matches_storage_class(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c00a3a509824b72d9870fe44d7bc0a330fcb61c8f4dd6708d4c3788acffa7dfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchesStorageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchesSuffix")
    def matches_suffix(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchesSuffix"))

    @matches_suffix.setter
    def matches_suffix(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba16692e13bd8ab1f396e6ad7229d096a5ba44cde648baaaf55117b99adede11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchesSuffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noncurrentTimeBefore")
    def noncurrent_time_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "noncurrentTimeBefore"))

    @noncurrent_time_before.setter
    def noncurrent_time_before(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf80ecf4ec3a657ae28bd5b5194ebda92283f9bbaafe956d5a271db5a073ba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noncurrentTimeBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numNewerVersions")
    def num_newer_versions(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numNewerVersions"))

    @num_newer_versions.setter
    def num_newer_versions(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae94a270423d5fa9881c2a32883764bf55a1c2874e2a7aa4efd7ed43ff47e3c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numNewerVersions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendAgeIfZero")
    def send_age_if_zero(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendAgeIfZero"))

    @send_age_if_zero.setter
    def send_age_if_zero(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d959d28d4a4d4f8c14410bc4530aa43a66484590feedcc564b47d76ecbd3b963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendAgeIfZero", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendDaysSinceCustomTimeIfZero")
    def send_days_since_custom_time_if_zero(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendDaysSinceCustomTimeIfZero"))

    @send_days_since_custom_time_if_zero.setter
    def send_days_since_custom_time_if_zero(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__131c50fb3101aa491d54cfcc265f38fa1c8c88b7b14f3dc56f9a999826fe9527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendDaysSinceCustomTimeIfZero", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendDaysSinceNoncurrentTimeIfZero")
    def send_days_since_noncurrent_time_if_zero(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendDaysSinceNoncurrentTimeIfZero"))

    @send_days_since_noncurrent_time_if_zero.setter
    def send_days_since_noncurrent_time_if_zero(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0335797ab4aa6c3dfde3bb13e7057075a3219093c158e9b3f90c227e44621f50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendDaysSinceNoncurrentTimeIfZero", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendNumNewerVersionsIfZero")
    def send_num_newer_versions_if_zero(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendNumNewerVersionsIfZero"))

    @send_num_newer_versions_if_zero.setter
    def send_num_newer_versions_if_zero(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb538d71b2295cca21feac44a011a91e206c9739328ba890e7b3ac9526ac924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendNumNewerVersionsIfZero", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withState")
    def with_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "withState"))

    @with_state.setter
    def with_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b351afd1a84e2bf5fa71241a00889dfce2bce90fd4fcfbe3b1b6c997d8a5667)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageBucketLifecycleRuleCondition]:
        return typing.cast(typing.Optional[GoogleStorageBucketLifecycleRuleCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBucketLifecycleRuleCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c090f331042bf79c8ab3da0c76902a2855935391f8a5c48d8ab65185f1eda74d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleStorageBucketLifecycleRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketLifecycleRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a83e3e95c719571a0c8e860a28eac145080f86864db760fcd2b0c7f50ca0fa9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleStorageBucketLifecycleRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c92f837aa179de9a4790fd36083306b162d2d832f4dbdd8a8bc6db937c915eb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleStorageBucketLifecycleRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3659c230c36b770916f7e96c83dde70223f79133b40123158ca3c36aa7d41ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0020a197d68a6be4d3b89ad7413f5af62e54bae8a26ddc4f19143589b0b70224)
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
            type_hints = typing.get_type_hints(_typecheckingstub__721cb5dcc9a6178b225a397650750c4d768692607bc316c32eba7fe5cbe40f94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageBucketLifecycleRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageBucketLifecycleRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageBucketLifecycleRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d7f09e28a0a796100fa35ab47ce22422da9bce83c972cc2091c8beb97cc4c6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleStorageBucketLifecycleRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketLifecycleRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8da4e3930000af8c94d7787a9c318826b5cf155e8ce1a8b6375dac6f6e54b363)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        type: builtins.str,
        storage_class: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: The type of the action of this Lifecycle Rule. Supported values include: Delete, SetStorageClass and AbortIncompleteMultipartUpload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#type GoogleStorageBucket#type}
        :param storage_class: The target Storage Class of objects affected by this Lifecycle Rule. Supported values include: MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#storage_class GoogleStorageBucket#storage_class}
        '''
        value = GoogleStorageBucketLifecycleRuleAction(
            type=type, storage_class=storage_class
        )

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        age: typing.Optional[jsii.Number] = None,
        created_before: typing.Optional[builtins.str] = None,
        custom_time_before: typing.Optional[builtins.str] = None,
        days_since_custom_time: typing.Optional[jsii.Number] = None,
        days_since_noncurrent_time: typing.Optional[jsii.Number] = None,
        matches_prefix: typing.Optional[typing.Sequence[builtins.str]] = None,
        matches_storage_class: typing.Optional[typing.Sequence[builtins.str]] = None,
        matches_suffix: typing.Optional[typing.Sequence[builtins.str]] = None,
        noncurrent_time_before: typing.Optional[builtins.str] = None,
        num_newer_versions: typing.Optional[jsii.Number] = None,
        send_age_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_days_since_custom_time_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_days_since_noncurrent_time_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_num_newer_versions_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        with_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param age: Minimum age of an object in days to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#age GoogleStorageBucket#age}
        :param created_before: Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#created_before GoogleStorageBucket#created_before}
        :param custom_time_before: Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#custom_time_before GoogleStorageBucket#custom_time_before}
        :param days_since_custom_time: Number of days elapsed since the user-specified timestamp set on an object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#days_since_custom_time GoogleStorageBucket#days_since_custom_time}
        :param days_since_noncurrent_time: Number of days elapsed since the noncurrent timestamp of an object. This condition is relevant only for versioned objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#days_since_noncurrent_time GoogleStorageBucket#days_since_noncurrent_time}
        :param matches_prefix: One or more matching name prefixes to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#matches_prefix GoogleStorageBucket#matches_prefix}
        :param matches_storage_class: Storage Class of objects to satisfy this condition. Supported values include: MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE, STANDARD, DURABLE_REDUCED_AVAILABILITY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#matches_storage_class GoogleStorageBucket#matches_storage_class}
        :param matches_suffix: One or more matching name suffixes to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#matches_suffix GoogleStorageBucket#matches_suffix}
        :param noncurrent_time_before: Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#noncurrent_time_before GoogleStorageBucket#noncurrent_time_before}
        :param num_newer_versions: Relevant only for versioned objects. The number of newer versions of an object to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#num_newer_versions GoogleStorageBucket#num_newer_versions}
        :param send_age_if_zero: While set true, age value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the age field. It can be used alone or together with age. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#send_age_if_zero GoogleStorageBucket#send_age_if_zero}
        :param send_days_since_custom_time_if_zero: While set true, days_since_custom_time value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the days_since_custom_time field. It can be used alone or together with days_since_custom_time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#send_days_since_custom_time_if_zero GoogleStorageBucket#send_days_since_custom_time_if_zero}
        :param send_days_since_noncurrent_time_if_zero: While set true, days_since_noncurrent_time value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the days_since_noncurrent_time field. It can be used alone or together with days_since_noncurrent_time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#send_days_since_noncurrent_time_if_zero GoogleStorageBucket#send_days_since_noncurrent_time_if_zero}
        :param send_num_newer_versions_if_zero: While set true, num_newer_versions value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the num_newer_versions field. It can be used alone or together with num_newer_versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#send_num_newer_versions_if_zero GoogleStorageBucket#send_num_newer_versions_if_zero}
        :param with_state: Match to live and/or archived objects. Unversioned buckets have only live objects. Supported values include: "LIVE", "ARCHIVED", "ANY". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#with_state GoogleStorageBucket#with_state}
        '''
        value = GoogleStorageBucketLifecycleRuleCondition(
            age=age,
            created_before=created_before,
            custom_time_before=custom_time_before,
            days_since_custom_time=days_since_custom_time,
            days_since_noncurrent_time=days_since_noncurrent_time,
            matches_prefix=matches_prefix,
            matches_storage_class=matches_storage_class,
            matches_suffix=matches_suffix,
            noncurrent_time_before=noncurrent_time_before,
            num_newer_versions=num_newer_versions,
            send_age_if_zero=send_age_if_zero,
            send_days_since_custom_time_if_zero=send_days_since_custom_time_if_zero,
            send_days_since_noncurrent_time_if_zero=send_days_since_noncurrent_time_if_zero,
            send_num_newer_versions_if_zero=send_num_newer_versions_if_zero,
            with_state=with_state,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> GoogleStorageBucketLifecycleRuleActionOutputReference:
        return typing.cast(GoogleStorageBucketLifecycleRuleActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> GoogleStorageBucketLifecycleRuleConditionOutputReference:
        return typing.cast(GoogleStorageBucketLifecycleRuleConditionOutputReference, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[GoogleStorageBucketLifecycleRuleAction]:
        return typing.cast(typing.Optional[GoogleStorageBucketLifecycleRuleAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[GoogleStorageBucketLifecycleRuleCondition]:
        return typing.cast(typing.Optional[GoogleStorageBucketLifecycleRuleCondition], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketLifecycleRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketLifecycleRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketLifecycleRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b121f92527510e3a8ed4385e047ba028b12b94081ee901b5408b3d8c690ef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketLogging",
    jsii_struct_bases=[],
    name_mapping={"log_bucket": "logBucket", "log_object_prefix": "logObjectPrefix"},
)
class GoogleStorageBucketLogging:
    def __init__(
        self,
        *,
        log_bucket: builtins.str,
        log_object_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_bucket: The bucket that will receive log objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#log_bucket GoogleStorageBucket#log_bucket}
        :param log_object_prefix: The object prefix for log objects. If it's not provided, by default Google Cloud Storage sets this to this bucket's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#log_object_prefix GoogleStorageBucket#log_object_prefix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8919d48ca750d4c8bc79a5b341d4284357f3dbd052588080d8fe8f9faad5c1ee)
            check_type(argname="argument log_bucket", value=log_bucket, expected_type=type_hints["log_bucket"])
            check_type(argname="argument log_object_prefix", value=log_object_prefix, expected_type=type_hints["log_object_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_bucket": log_bucket,
        }
        if log_object_prefix is not None:
            self._values["log_object_prefix"] = log_object_prefix

    @builtins.property
    def log_bucket(self) -> builtins.str:
        '''The bucket that will receive log objects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#log_bucket GoogleStorageBucket#log_bucket}
        '''
        result = self._values.get("log_bucket")
        assert result is not None, "Required property 'log_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_object_prefix(self) -> typing.Optional[builtins.str]:
        '''The object prefix for log objects.

        If it's not provided, by default Google Cloud Storage sets this to this bucket's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#log_object_prefix GoogleStorageBucket#log_object_prefix}
        '''
        result = self._values.get("log_object_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketLogging(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketLoggingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketLoggingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69ed3be1b6874962224e1965d926fb3473d90a756dcfc6fc352659012c463a61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLogObjectPrefix")
    def reset_log_object_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogObjectPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="logBucketInput")
    def log_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="logObjectPrefixInput")
    def log_object_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logObjectPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="logBucket")
    def log_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logBucket"))

    @log_bucket.setter
    def log_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba0a8cb20479dbc9b7aaebaf8473302b15a767a4ed68b672dc4c71d4af32d63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logObjectPrefix")
    def log_object_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logObjectPrefix"))

    @log_object_prefix.setter
    def log_object_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f4913b0e0747615569091ff18ae641dbe8746c826ce79a50d6b4f41697b224)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logObjectPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleStorageBucketLogging]:
        return typing.cast(typing.Optional[GoogleStorageBucketLogging], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBucketLogging],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41368920bb1c39bb1378157fdf76518f5ad754bd1dee9e5f3d517b066726d5c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={"retention_period": "retentionPeriod", "is_locked": "isLocked"},
)
class GoogleStorageBucketRetentionPolicy:
    def __init__(
        self,
        *,
        retention_period: jsii.Number,
        is_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param retention_period: The period of time, in seconds, that objects in the bucket must be retained and cannot be deleted, overwritten, or archived. The value must be less than 3,155,760,000 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#retention_period GoogleStorageBucket#retention_period}
        :param is_locked: If set to true, the bucket will be locked and permanently restrict edits to the bucket's retention policy. Caution: Locking a bucket is an irreversible action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#is_locked GoogleStorageBucket#is_locked}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f313535967b0e78f2094fb5283866c12dcd7893d52f091056d84b2537fb67202)
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            check_type(argname="argument is_locked", value=is_locked, expected_type=type_hints["is_locked"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "retention_period": retention_period,
        }
        if is_locked is not None:
            self._values["is_locked"] = is_locked

    @builtins.property
    def retention_period(self) -> jsii.Number:
        '''The period of time, in seconds, that objects in the bucket must be retained and cannot be deleted, overwritten, or archived.

        The value must be less than 3,155,760,000 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#retention_period GoogleStorageBucket#retention_period}
        '''
        result = self._values.get("retention_period")
        assert result is not None, "Required property 'retention_period' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def is_locked(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the bucket will be locked and permanently restrict edits to the bucket's retention policy.

        Caution: Locking a bucket is an irreversible action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#is_locked GoogleStorageBucket#is_locked}
        '''
        result = self._values.get("is_locked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03169d60c76fa645c60201fa9fac8a916c6eb894111136225ffb78c26342c46e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsLocked")
    def reset_is_locked(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsLocked", []))

    @builtins.property
    @jsii.member(jsii_name="isLockedInput")
    def is_locked_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isLockedInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodInput")
    def retention_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="isLocked")
    def is_locked(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isLocked"))

    @is_locked.setter
    def is_locked(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b23537f4b69eb4aec3cab2cdca0d1a276324a39bef0a193bf63d85281219c7f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isLocked", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPeriod")
    def retention_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriod"))

    @retention_period.setter
    def retention_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4405c099d2820418b46406f549d1e02aecc7b717fde2a3146f3bfbab1343b2cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleStorageBucketRetentionPolicy]:
        return typing.cast(typing.Optional[GoogleStorageBucketRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBucketRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02fdfdd5d97758ec36d0679f01ae8ba5ba3a557f7cbcce7b33b2431c9a3595e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketSoftDeletePolicy",
    jsii_struct_bases=[],
    name_mapping={"retention_duration_seconds": "retentionDurationSeconds"},
)
class GoogleStorageBucketSoftDeletePolicy:
    def __init__(
        self,
        *,
        retention_duration_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param retention_duration_seconds: The duration in seconds that soft-deleted objects in the bucket will be retained and cannot be permanently deleted. Default value is 604800. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#retention_duration_seconds GoogleStorageBucket#retention_duration_seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d666ad6bb00f86aacdcb484ecfa1fbdf9e66644af661e7e98cf33b04ca9c77)
            check_type(argname="argument retention_duration_seconds", value=retention_duration_seconds, expected_type=type_hints["retention_duration_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if retention_duration_seconds is not None:
            self._values["retention_duration_seconds"] = retention_duration_seconds

    @builtins.property
    def retention_duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''The duration in seconds that soft-deleted objects in the bucket will be retained and cannot be permanently deleted.

        Default value is 604800.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#retention_duration_seconds GoogleStorageBucket#retention_duration_seconds}
        '''
        result = self._values.get("retention_duration_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketSoftDeletePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketSoftDeletePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketSoftDeletePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbe48c761d7ef65995ad909e72df02c4c5766c56b84134c584a68422ba5d4473)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRetentionDurationSeconds")
    def reset_retention_duration_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionDurationSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="effectiveTime")
    def effective_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveTime"))

    @builtins.property
    @jsii.member(jsii_name="retentionDurationSecondsInput")
    def retention_duration_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionDurationSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionDurationSeconds")
    def retention_duration_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionDurationSeconds"))

    @retention_duration_seconds.setter
    def retention_duration_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c5d361f74d4e455b4a4cf6334f45e3390ef9512a7ee47ce0625fcd3daf59b04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDurationSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleStorageBucketSoftDeletePolicy]:
        return typing.cast(typing.Optional[GoogleStorageBucketSoftDeletePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBucketSoftDeletePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c38caf1836c076ba3be1f1b6176be5daf1c45a9bc49dd3aa6d3b5be842aec60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "read": "read", "update": "update"},
)
class GoogleStorageBucketTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#create GoogleStorageBucket#create}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#read GoogleStorageBucket#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#update GoogleStorageBucket#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66d2ca6785932c05178cdbada82417557ded560367a202dbd5097fc5e277a862)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#create GoogleStorageBucket#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#read GoogleStorageBucket#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#update GoogleStorageBucket#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50008b0b02d078667e5b69095a02f04d35ae1f3db1ead28e49fe701072ec5a73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4445e52b4be4bed282034a8b51c0826019f164659bd32aa4416b475b81186382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1807175511635c1e14adbc7ec771af8e104c93ce6bf3bb67a24e0d0081c912cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7657c5af709d69f48d8d69d2e90b594be8923be4716131b22906b8a8e3111c7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcfb7b0c44d18aed8a4b3e0d84b21d769e1fa9c6c05c9c5337969a515214259f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketVersioning",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleStorageBucketVersioning:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: While set to true, versioning is fully enabled for this bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#enabled GoogleStorageBucket#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff0bb706391cc8df817781b36a13f4a6f1fd07ff64058b3543b76b688c9268b)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''While set to true, versioning is fully enabled for this bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#enabled GoogleStorageBucket#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketVersioning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketVersioningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketVersioningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a85cb0b04cd02e073fb467f90db88335e0f19ace8500aeb377cb4091c2ca617e)
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
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bfdac444c5f930b23c16c1398962c986b43fed5208d6bd9c7abc564b378fcbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleStorageBucketVersioning]:
        return typing.cast(typing.Optional[GoogleStorageBucketVersioning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBucketVersioning],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7538afeba461099dad88ce9fc439aefd6dbaa843c7710515cb3d4267e45a4b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketWebsite",
    jsii_struct_bases=[],
    name_mapping={
        "main_page_suffix": "mainPageSuffix",
        "not_found_page": "notFoundPage",
    },
)
class GoogleStorageBucketWebsite:
    def __init__(
        self,
        *,
        main_page_suffix: typing.Optional[builtins.str] = None,
        not_found_page: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param main_page_suffix: Behaves as the bucket's directory index where missing objects are treated as potential directories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#main_page_suffix GoogleStorageBucket#main_page_suffix}
        :param not_found_page: The custom object to return when a requested resource is not found. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#not_found_page GoogleStorageBucket#not_found_page}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6109dd7e1e6356ebca39d46399d08b4708b9c37f31694f66dc3658bcf65d962)
            check_type(argname="argument main_page_suffix", value=main_page_suffix, expected_type=type_hints["main_page_suffix"])
            check_type(argname="argument not_found_page", value=not_found_page, expected_type=type_hints["not_found_page"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if main_page_suffix is not None:
            self._values["main_page_suffix"] = main_page_suffix
        if not_found_page is not None:
            self._values["not_found_page"] = not_found_page

    @builtins.property
    def main_page_suffix(self) -> typing.Optional[builtins.str]:
        '''Behaves as the bucket's directory index where missing objects are treated as potential directories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#main_page_suffix GoogleStorageBucket#main_page_suffix}
        '''
        result = self._values.get("main_page_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def not_found_page(self) -> typing.Optional[builtins.str]:
        '''The custom object to return when a requested resource is not found.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_bucket#not_found_page GoogleStorageBucket#not_found_page}
        '''
        result = self._values.get("not_found_page")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageBucketWebsite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageBucketWebsiteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageBucket.GoogleStorageBucketWebsiteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aad1bef17de9c218841dea23199f8efec19c845686a7c2c734ca4a3f30e70962)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMainPageSuffix")
    def reset_main_page_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainPageSuffix", []))

    @jsii.member(jsii_name="resetNotFoundPage")
    def reset_not_found_page(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotFoundPage", []))

    @builtins.property
    @jsii.member(jsii_name="mainPageSuffixInput")
    def main_page_suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainPageSuffixInput"))

    @builtins.property
    @jsii.member(jsii_name="notFoundPageInput")
    def not_found_page_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notFoundPageInput"))

    @builtins.property
    @jsii.member(jsii_name="mainPageSuffix")
    def main_page_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainPageSuffix"))

    @main_page_suffix.setter
    def main_page_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb0f0fad0017f560596096f6bd623246397216f566294cbe1ae9e1799889aea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainPageSuffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notFoundPage")
    def not_found_page(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notFoundPage"))

    @not_found_page.setter
    def not_found_page(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d450a5d66b726d59207c410f03cba0489a94fa1ae3e535c9d9a3f3ddc7e817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notFoundPage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleStorageBucketWebsite]:
        return typing.cast(typing.Optional[GoogleStorageBucketWebsite], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageBucketWebsite],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b967459eb705a3225d3719bbfd32d8440e4eb3c59f800508a51588809185c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleStorageBucket",
    "GoogleStorageBucketAutoclass",
    "GoogleStorageBucketAutoclassOutputReference",
    "GoogleStorageBucketConfig",
    "GoogleStorageBucketCors",
    "GoogleStorageBucketCorsList",
    "GoogleStorageBucketCorsOutputReference",
    "GoogleStorageBucketCustomPlacementConfig",
    "GoogleStorageBucketCustomPlacementConfigOutputReference",
    "GoogleStorageBucketEncryption",
    "GoogleStorageBucketEncryptionOutputReference",
    "GoogleStorageBucketHierarchicalNamespace",
    "GoogleStorageBucketHierarchicalNamespaceOutputReference",
    "GoogleStorageBucketIpFilter",
    "GoogleStorageBucketIpFilterOutputReference",
    "GoogleStorageBucketIpFilterPublicNetworkSource",
    "GoogleStorageBucketIpFilterPublicNetworkSourceOutputReference",
    "GoogleStorageBucketIpFilterVpcNetworkSources",
    "GoogleStorageBucketIpFilterVpcNetworkSourcesList",
    "GoogleStorageBucketIpFilterVpcNetworkSourcesOutputReference",
    "GoogleStorageBucketLifecycleRule",
    "GoogleStorageBucketLifecycleRuleAction",
    "GoogleStorageBucketLifecycleRuleActionOutputReference",
    "GoogleStorageBucketLifecycleRuleCondition",
    "GoogleStorageBucketLifecycleRuleConditionOutputReference",
    "GoogleStorageBucketLifecycleRuleList",
    "GoogleStorageBucketLifecycleRuleOutputReference",
    "GoogleStorageBucketLogging",
    "GoogleStorageBucketLoggingOutputReference",
    "GoogleStorageBucketRetentionPolicy",
    "GoogleStorageBucketRetentionPolicyOutputReference",
    "GoogleStorageBucketSoftDeletePolicy",
    "GoogleStorageBucketSoftDeletePolicyOutputReference",
    "GoogleStorageBucketTimeouts",
    "GoogleStorageBucketTimeoutsOutputReference",
    "GoogleStorageBucketVersioning",
    "GoogleStorageBucketVersioningOutputReference",
    "GoogleStorageBucketWebsite",
    "GoogleStorageBucketWebsiteOutputReference",
]

publication.publish()

def _typecheckingstub__a96b01c7750cdefb3fba97844d4f02a4010e6bcb00ea6e5f27e6cea37c7f6e28(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    autoclass: typing.Optional[typing.Union[GoogleStorageBucketAutoclass, typing.Dict[builtins.str, typing.Any]]] = None,
    cors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleStorageBucketCors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_placement_config: typing.Optional[typing.Union[GoogleStorageBucketCustomPlacementConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_event_based_hold: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_object_retention: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption: typing.Optional[typing.Union[GoogleStorageBucketEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hierarchical_namespace: typing.Optional[typing.Union[GoogleStorageBucketHierarchicalNamespace, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_filter: typing.Optional[typing.Union[GoogleStorageBucketIpFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleStorageBucketLifecycleRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    logging: typing.Optional[typing.Union[GoogleStorageBucketLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    public_access_prevention: typing.Optional[builtins.str] = None,
    requester_pays: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retention_policy: typing.Optional[typing.Union[GoogleStorageBucketRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    rpo: typing.Optional[builtins.str] = None,
    soft_delete_policy: typing.Optional[typing.Union[GoogleStorageBucketSoftDeletePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_class: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleStorageBucketTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    uniform_bucket_level_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    versioning: typing.Optional[typing.Union[GoogleStorageBucketVersioning, typing.Dict[builtins.str, typing.Any]]] = None,
    website: typing.Optional[typing.Union[GoogleStorageBucketWebsite, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ac8199978729f9d2216be606073c97cbf214d839092f96b450d40c00e3c89311(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86dc3c42f9665643610073bdacf287de6f68ca9daa71c8ecf04d6d6694a972c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleStorageBucketCors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d85c194504e5578dcb0bc3b72c80b9882370c23fdd6440c7d90a3e9688373f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleStorageBucketLifecycleRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__534bb0e91dcdf26648981490ff48446eb6747b98609a9399c0248c41a39e3987(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5655ef99ccd361bcbd45b9f62e262cbec97e97c0467c065743c9f69bed645bc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3037e124abb7cd3a7a5b7d7667a52809eb628386d78da504fb43b05a4642a33b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0863af05a34e34384a3fecedfd0a74c96fd2897e7dbe2ab0b942a85f5ae83232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9da57b75f3e411ca65a3304f309d00a97f4bf72e118914d4c98d42eec260fe(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a05b8eb66bf2544a271ac0bf7706868f6e357468ac21fc8e895e3319e1f67f75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9561046b88c653b419817d6e197f342b6637ecdb2c559f50f36e8baba7e2b73a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58f15dac6100a76cd00c99d6479a0e498419e427bb137c4464c4deb8bbe3d468(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b4302fccb6f81a5e30afa6c06063f970a9087e1bfad15d668ed333ea292570(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19086bcdeb6b2a3c97427819dfff62b5e381ef3d8e5620690e4d6bbcbe911a2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fefd0e6c984446e81222637dc9cbf800fc2d2a6db4b994d5ce11dcc31b4b38f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a68a1710af04cdcd3cdb188187b334d83b5a46427d6cfed40061ead17a00f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f0228bad12bec8950e878585ca6c609ebb135ce00c4a4921a601dffe5f88e5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1d333df0da0eb61948e89deb3c0d6ca6110864821ee392602744ef26ef03f3(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    terminal_storage_class: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdcafb7b1f73587c4e444f55434d9b6bbe14be1562382704f19f4430100f0256(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bdbe11e4ed1f582a872fa13417b3a4d29ff9c05286bc4dae706cd65707e574(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d913e77ab6c610fda8613945514134abca3d37e08d6486cea2c5e4f032bcaaa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7611b557e9b3825a4332fad225343cc5021bfae6f3e8a1e486bc41760d7cf426(
    value: typing.Optional[GoogleStorageBucketAutoclass],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3623721f62b375d44511fb3c7e51f92199d618059b7a77a5062075147e8cae2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    autoclass: typing.Optional[typing.Union[GoogleStorageBucketAutoclass, typing.Dict[builtins.str, typing.Any]]] = None,
    cors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleStorageBucketCors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_placement_config: typing.Optional[typing.Union[GoogleStorageBucketCustomPlacementConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_event_based_hold: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_object_retention: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption: typing.Optional[typing.Union[GoogleStorageBucketEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hierarchical_namespace: typing.Optional[typing.Union[GoogleStorageBucketHierarchicalNamespace, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_filter: typing.Optional[typing.Union[GoogleStorageBucketIpFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleStorageBucketLifecycleRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    logging: typing.Optional[typing.Union[GoogleStorageBucketLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    public_access_prevention: typing.Optional[builtins.str] = None,
    requester_pays: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retention_policy: typing.Optional[typing.Union[GoogleStorageBucketRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    rpo: typing.Optional[builtins.str] = None,
    soft_delete_policy: typing.Optional[typing.Union[GoogleStorageBucketSoftDeletePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_class: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleStorageBucketTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    uniform_bucket_level_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    versioning: typing.Optional[typing.Union[GoogleStorageBucketVersioning, typing.Dict[builtins.str, typing.Any]]] = None,
    website: typing.Optional[typing.Union[GoogleStorageBucketWebsite, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cc81faf65f2ea3a53c738ac18d03e6dbd526761949c092e21a57efc0ebc5b2(
    *,
    max_age_seconds: typing.Optional[jsii.Number] = None,
    method: typing.Optional[typing.Sequence[builtins.str]] = None,
    origin: typing.Optional[typing.Sequence[builtins.str]] = None,
    response_header: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29d650083baecfe4ce34c1a39ec4eff283dbd0b2d6b47d4ad5c3b45f2e75cfa5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e773c059aef636a85ab61356e37afb680dacec910241876b5ddb7388e7afa06(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eeae2b6eaf08292574fe559c1eeedc7f74dfa21b3c2b061ee7e3bf4af821416(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bef737a34de97248a8959020056ade164453f39cd4357f76009ca22df5acbb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b626fec4d1c9251a4594f63cb583205110d50cb55fe4c0507506603350fa21f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d7ac1cb1cad9ed3382bf17d9d6b4d53172274dd1ca19832662a4a6c18e0f32(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageBucketCors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9a24725956a2509162eaf45e98ec7297c791533c7b4a4b0aead881c4547b0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89bcae2dc30121dbe0a5bf049a3ffe239e12f218039c2e62100fd04dfa8303f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e08391c96391e72c5a919163d7db239873546bff1a8d599f94bbc10db908e64(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c52c6dc8b9a0193d2f1fab192bfb83c963b9bd7131666b898423e22aab23a6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a3404ac321e63c9f0fff6249ff4180a7fec01f805df1791aed40b56adcdb6a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa6dc66e9f5d25c553465713e04e0f59be329693430e5773d155811b9836244(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketCors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3505625673f21db4874ba0436a05b091f1597e94ffc3181d927a9fb83357b84(
    *,
    data_locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c3c75aee6b8d81806dcbd0730c18a21a1b7aa6a8bcf32b224bafa695ecd285(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ef5b9f3d596ec9c8fa718cb048fffbbdcc5ba5c53fe4e57e7547e85b43dd08(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0a67149444e2556c43af5559d72a90856f1cdf204653b76dc648efc31e611a(
    value: typing.Optional[GoogleStorageBucketCustomPlacementConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4afb464e305051d9ee9b623daa22e6bd68ea76688ee9ac878dfc932742862a16(
    *,
    default_kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155b617c67cc1eae002aaf18e88814036514deb39cfb18b7aa4c7ef15d111a59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032c68510a5048508ea0028f88fc09719c1eea051de66c0aeaf837b70ca8edbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a8f0d5fc564596d46016fb74324d0bdbd1e79a129a9aac413e20c065c78d59(
    value: typing.Optional[GoogleStorageBucketEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394d06d860fd468468bbc838904a1682b88959b92ca5d21ca6d2c1f8f3a7e460(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e709e90fac1459f2c333b63a80b1f57e41d043663e8d3cf1668f9d19da370a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a491432a96a870691334a65746297b8f8d278157e1e84e00de4a5a57b9928679(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7f56df3c15ee4746f692e73724cdb98f784571c3ed17cda9d4f85d208ad5d4(
    value: typing.Optional[GoogleStorageBucketHierarchicalNamespace],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40da5b3d77655a384e56f9dc4044d4770d4398dadf61f93098e5ab6c279cdc8e(
    *,
    mode: builtins.str,
    public_network_source: typing.Optional[typing.Union[GoogleStorageBucketIpFilterPublicNetworkSource, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_network_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleStorageBucketIpFilterVpcNetworkSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991138c050c70ddefa91b6ffd902812515ad56bdba8e6d1e2de61135d64e4725(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9786742d92b3b598596679d732da484e0f2df2f86c4f00c9f62263bb4492d9eb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleStorageBucketIpFilterVpcNetworkSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7fe79326f1243c9ca974331cea65663b011335ab175ff04bebc951c2d52e4e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272f4997866ca483499993c2f355b61f04f26196b2eb5c9c43d0a6f5cae3e525(
    value: typing.Optional[GoogleStorageBucketIpFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9afeafc87bc7c63c72f37b0391aee1b9835287c959f366f33f18bdab7cd882ea(
    *,
    allowed_ip_cidr_ranges: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740b4aeb4584b29ded363eef0fca16d893b38007e9af3848653760d78e29762a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd7228308ccabaae57845ddd25dec366f42de630b6bfec48a29a08020af9e3b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a918474a8d141269a52177610c18729a2c7c6a92e652af41d89049cd493d0718(
    value: typing.Optional[GoogleStorageBucketIpFilterPublicNetworkSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b97b37f6b247df9e8407bb807fc87c005d60528ea6980881fdf1db2b5db8a5(
    *,
    allowed_ip_cidr_ranges: typing.Sequence[builtins.str],
    network: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5808e359de6d3ea9480b9127e16d7e98a79c4151317861f829665b261e695de9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5ad6137b1ec722b9b735451db7e4748e73db74114933659261f756363e73e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ec7250857ad9937ec3c21c96c384ff483900accda7241d00d32c653f99779fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf36f0c3ebe78a05b484ca97d0c0fadecce1368cb1f4a7f321ba2631722ba50(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e79cfdcc12557fc894d04fab4fc516ad018e1e73048dea787e9f86b225a249b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769cecfa807df146ef8b637edc0511b65a5441ba8a06eea22c51f7add540b8c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageBucketIpFilterVpcNetworkSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75843a1b4d6c3b9d504e923e4440a283529e04edad810cac95234e1227df88fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33fd38c970f7e56eeaed5cfbcfa75760361f5e57392fa1c3d3af544b2424936e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c3e22755a4bae2d0b5ce98c498291f2db7732d4cfb3dc076395b7dde97a161a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e0142e1dfdf35768ab177489662aed5fc0a5ae17053550c82c84138b6cc065(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketIpFilterVpcNetworkSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8d36e84494c14e7380db271694c87dacbe1c2e103075ca47494ebf50d88ed8(
    *,
    action: typing.Union[GoogleStorageBucketLifecycleRuleAction, typing.Dict[builtins.str, typing.Any]],
    condition: typing.Union[GoogleStorageBucketLifecycleRuleCondition, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b3ac7d760d045f0448d968562b532414e1d4a60964aaa8c857ee09e42f06dc(
    *,
    type: builtins.str,
    storage_class: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccdf950211915ad9a10cd42f5b5e04705bd2115603001951c58032eab163f735(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50db44fc996b8b85559a846d29b9e2a9826ed25eb4fe0d8eec70ddfbc0ab873(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2defb3cdc3f0e3e06a8a4643bb9a49553c8459c3436d0bf559f2d36b26660572(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03bd90466ae7033d71d27730e045147739fd5344602c003609f177f545fd63ff(
    value: typing.Optional[GoogleStorageBucketLifecycleRuleAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bfb170d9bff6a49b44134faf5b950d91e1a3958f05ecf519f2fd153f633be8(
    *,
    age: typing.Optional[jsii.Number] = None,
    created_before: typing.Optional[builtins.str] = None,
    custom_time_before: typing.Optional[builtins.str] = None,
    days_since_custom_time: typing.Optional[jsii.Number] = None,
    days_since_noncurrent_time: typing.Optional[jsii.Number] = None,
    matches_prefix: typing.Optional[typing.Sequence[builtins.str]] = None,
    matches_storage_class: typing.Optional[typing.Sequence[builtins.str]] = None,
    matches_suffix: typing.Optional[typing.Sequence[builtins.str]] = None,
    noncurrent_time_before: typing.Optional[builtins.str] = None,
    num_newer_versions: typing.Optional[jsii.Number] = None,
    send_age_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_days_since_custom_time_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_days_since_noncurrent_time_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_num_newer_versions_if_zero: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    with_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ebde1e1121464bd8c2a2fbc36b6edff413f4c1bda03936679437c31476b524(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726c5c4b3f115a675983875e43e10f3ee94719f2958f15e999151c599c559c75(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a92d0877fd3bc759e4f3163cb0f18530c5cd8767696f8c9ecf889c2e03eba8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946beba83a867cc21efed880a1baf6b78dae8610da896b745120c54ac38d399e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c89b9fde9a002fc8ea41f4757f5938e318409f9aab4bd54aa65fba47a6da18f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3c55dccfd288a6f7bee6d828d61569ca8d536b006477c17718fde12f85930f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94db5fb467d1e4bee8db7f85e9927c544886d3d0dde960ef4276b2ea4a6b1d6e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00a3a509824b72d9870fe44d7bc0a330fcb61c8f4dd6708d4c3788acffa7dfe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba16692e13bd8ab1f396e6ad7229d096a5ba44cde648baaaf55117b99adede11(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf80ecf4ec3a657ae28bd5b5194ebda92283f9bbaafe956d5a271db5a073ba7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae94a270423d5fa9881c2a32883764bf55a1c2874e2a7aa4efd7ed43ff47e3c0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d959d28d4a4d4f8c14410bc4530aa43a66484590feedcc564b47d76ecbd3b963(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131c50fb3101aa491d54cfcc265f38fa1c8c88b7b14f3dc56f9a999826fe9527(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0335797ab4aa6c3dfde3bb13e7057075a3219093c158e9b3f90c227e44621f50(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb538d71b2295cca21feac44a011a91e206c9739328ba890e7b3ac9526ac924(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b351afd1a84e2bf5fa71241a00889dfce2bce90fd4fcfbe3b1b6c997d8a5667(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c090f331042bf79c8ab3da0c76902a2855935391f8a5c48d8ab65185f1eda74d(
    value: typing.Optional[GoogleStorageBucketLifecycleRuleCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83e3e95c719571a0c8e860a28eac145080f86864db760fcd2b0c7f50ca0fa9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c92f837aa179de9a4790fd36083306b162d2d832f4dbdd8a8bc6db937c915eb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3659c230c36b770916f7e96c83dde70223f79133b40123158ca3c36aa7d41ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0020a197d68a6be4d3b89ad7413f5af62e54bae8a26ddc4f19143589b0b70224(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721cb5dcc9a6178b225a397650750c4d768692607bc316c32eba7fe5cbe40f94(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7f09e28a0a796100fa35ab47ce22422da9bce83c972cc2091c8beb97cc4c6f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleStorageBucketLifecycleRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da4e3930000af8c94d7787a9c318826b5cf155e8ce1a8b6375dac6f6e54b363(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b121f92527510e3a8ed4385e047ba028b12b94081ee901b5408b3d8c690ef2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketLifecycleRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8919d48ca750d4c8bc79a5b341d4284357f3dbd052588080d8fe8f9faad5c1ee(
    *,
    log_bucket: builtins.str,
    log_object_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ed3be1b6874962224e1965d926fb3473d90a756dcfc6fc352659012c463a61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba0a8cb20479dbc9b7aaebaf8473302b15a767a4ed68b672dc4c71d4af32d63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f4913b0e0747615569091ff18ae641dbe8746c826ce79a50d6b4f41697b224(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41368920bb1c39bb1378157fdf76518f5ad754bd1dee9e5f3d517b066726d5c3(
    value: typing.Optional[GoogleStorageBucketLogging],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f313535967b0e78f2094fb5283866c12dcd7893d52f091056d84b2537fb67202(
    *,
    retention_period: jsii.Number,
    is_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03169d60c76fa645c60201fa9fac8a916c6eb894111136225ffb78c26342c46e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b23537f4b69eb4aec3cab2cdca0d1a276324a39bef0a193bf63d85281219c7f8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4405c099d2820418b46406f549d1e02aecc7b717fde2a3146f3bfbab1343b2cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02fdfdd5d97758ec36d0679f01ae8ba5ba3a557f7cbcce7b33b2431c9a3595e9(
    value: typing.Optional[GoogleStorageBucketRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d666ad6bb00f86aacdcb484ecfa1fbdf9e66644af661e7e98cf33b04ca9c77(
    *,
    retention_duration_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe48c761d7ef65995ad909e72df02c4c5766c56b84134c584a68422ba5d4473(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5d361f74d4e455b4a4cf6334f45e3390ef9512a7ee47ce0625fcd3daf59b04(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c38caf1836c076ba3be1f1b6176be5daf1c45a9bc49dd3aa6d3b5be842aec60(
    value: typing.Optional[GoogleStorageBucketSoftDeletePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d2ca6785932c05178cdbada82417557ded560367a202dbd5097fc5e277a862(
    *,
    create: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50008b0b02d078667e5b69095a02f04d35ae1f3db1ead28e49fe701072ec5a73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4445e52b4be4bed282034a8b51c0826019f164659bd32aa4416b475b81186382(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1807175511635c1e14adbc7ec771af8e104c93ce6bf3bb67a24e0d0081c912cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7657c5af709d69f48d8d69d2e90b594be8923be4716131b22906b8a8e3111c7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcfb7b0c44d18aed8a4b3e0d84b21d769e1fa9c6c05c9c5337969a515214259f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageBucketTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff0bb706391cc8df817781b36a13f4a6f1fd07ff64058b3543b76b688c9268b(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a85cb0b04cd02e073fb467f90db88335e0f19ace8500aeb377cb4091c2ca617e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bfdac444c5f930b23c16c1398962c986b43fed5208d6bd9c7abc564b378fcbb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7538afeba461099dad88ce9fc439aefd6dbaa843c7710515cb3d4267e45a4b4(
    value: typing.Optional[GoogleStorageBucketVersioning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6109dd7e1e6356ebca39d46399d08b4708b9c37f31694f66dc3658bcf65d962(
    *,
    main_page_suffix: typing.Optional[builtins.str] = None,
    not_found_page: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad1bef17de9c218841dea23199f8efec19c845686a7c2c734ca4a3f30e70962(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb0f0fad0017f560596096f6bd623246397216f566294cbe1ae9e1799889aea4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d450a5d66b726d59207c410f03cba0489a94fa1ae3e535c9d9a3f3ddc7e817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b967459eb705a3225d3719bbfd32d8440e4eb3c59f800508a51588809185c1(
    value: typing.Optional[GoogleStorageBucketWebsite],
) -> None:
    """Type checking stubs"""
    pass
