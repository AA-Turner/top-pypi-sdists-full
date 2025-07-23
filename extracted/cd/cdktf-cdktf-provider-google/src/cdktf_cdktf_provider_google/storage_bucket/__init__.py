r'''
# `google_storage_bucket`

Refer to the Terraform Registry for docs: [`google_storage_bucket`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket).
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


class StorageBucket(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucket",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket google_storage_bucket}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        autoclass: typing.Optional[typing.Union["StorageBucketAutoclass", typing.Dict[builtins.str, typing.Any]]] = None,
        cors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageBucketCors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_placement_config: typing.Optional[typing.Union["StorageBucketCustomPlacementConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_event_based_hold: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_object_retention: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption: typing.Optional[typing.Union["StorageBucketEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hierarchical_namespace: typing.Optional[typing.Union["StorageBucketHierarchicalNamespace", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_filter: typing.Optional[typing.Union["StorageBucketIpFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageBucketLifecycleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        logging: typing.Optional[typing.Union["StorageBucketLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        public_access_prevention: typing.Optional[builtins.str] = None,
        requester_pays: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_policy: typing.Optional[typing.Union["StorageBucketRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        rpo: typing.Optional[builtins.str] = None,
        soft_delete_policy: typing.Optional[typing.Union["StorageBucketSoftDeletePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_class: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StorageBucketTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        uniform_bucket_level_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        versioning: typing.Optional[typing.Union["StorageBucketVersioning", typing.Dict[builtins.str, typing.Any]]] = None,
        website: typing.Optional[typing.Union["StorageBucketWebsite", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket google_storage_bucket} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The Google Cloud Storage location or region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#location StorageBucket#location}
        :param name: The name of the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#name StorageBucket#name}
        :param autoclass: autoclass block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#autoclass StorageBucket#autoclass}
        :param cors: cors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#cors StorageBucket#cors}
        :param custom_placement_config: custom_placement_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#custom_placement_config StorageBucket#custom_placement_config}
        :param default_event_based_hold: Whether or not to automatically apply an eventBasedHold to new objects added to the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#default_event_based_hold StorageBucket#default_event_based_hold}
        :param enable_object_retention: Enables each object in the bucket to have its own retention policy, which prevents deletion until stored for a specific length of time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#enable_object_retention StorageBucket#enable_object_retention}
        :param encryption: encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#encryption StorageBucket#encryption}
        :param force_destroy: When deleting a bucket, this boolean option will delete all contained objects, or anywhereCaches (if any). If you try to delete a bucket that contains objects or anywhereCaches, Terraform will fail that run, deleting anywhereCaches may take 80 minutes to complete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#force_destroy StorageBucket#force_destroy}
        :param hierarchical_namespace: hierarchical_namespace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#hierarchical_namespace StorageBucket#hierarchical_namespace}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#id StorageBucket#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_filter: ip_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#ip_filter StorageBucket#ip_filter}
        :param labels: A set of key/value label pairs to assign to the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#labels StorageBucket#labels}
        :param lifecycle_rule: lifecycle_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#lifecycle_rule StorageBucket#lifecycle_rule}
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#logging StorageBucket#logging}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#project StorageBucket#project}
        :param public_access_prevention: Prevents public access to a bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#public_access_prevention StorageBucket#public_access_prevention}
        :param requester_pays: Enables Requester Pays on a storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#requester_pays StorageBucket#requester_pays}
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#retention_policy StorageBucket#retention_policy}
        :param rpo: Specifies the RPO setting of bucket. If set 'ASYNC_TURBO', The Turbo Replication will be enabled for the dual-region bucket. Value 'DEFAULT' will set RPO setting to default. Turbo Replication is only for buckets in dual-regions.See the docs for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#rpo StorageBucket#rpo}
        :param soft_delete_policy: soft_delete_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#soft_delete_policy StorageBucket#soft_delete_policy}
        :param storage_class: The Storage Class of the new bucket. Supported values include: STANDARD, MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#storage_class StorageBucket#storage_class}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#timeouts StorageBucket#timeouts}
        :param uniform_bucket_level_access: Enables uniform bucket-level access on a bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#uniform_bucket_level_access StorageBucket#uniform_bucket_level_access}
        :param versioning: versioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#versioning StorageBucket#versioning}
        :param website: website block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#website StorageBucket#website}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e744e8e397ebe7477262305eaa79414a8daecc81c0364a30bc93b0eeb7a4c659)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StorageBucketConfig(
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
        '''Generates CDKTF code for importing a StorageBucket resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StorageBucket to import.
        :param import_from_id: The id of the existing StorageBucket that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StorageBucket to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80def101596c1c23b9348b9c0ec04c4df1a1ca684d1d2e9a9c8f9cb4e155c86a)
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
        :param enabled: While set to true, autoclass automatically transitions objects in your bucket to appropriate storage classes based on each object's access pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#enabled StorageBucket#enabled}
        :param terminal_storage_class: The storage class that objects in the bucket eventually transition to if they are not read for a certain length of time. Supported values include: NEARLINE, ARCHIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#terminal_storage_class StorageBucket#terminal_storage_class}
        '''
        value = StorageBucketAutoclass(
            enabled=enabled, terminal_storage_class=terminal_storage_class
        )

        return typing.cast(None, jsii.invoke(self, "putAutoclass", [value]))

    @jsii.member(jsii_name="putCors")
    def put_cors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageBucketCors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d33be404b12e6bc299a9294405031bcde96d41876f6ef597a16bdd1c9084fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCors", [value]))

    @jsii.member(jsii_name="putCustomPlacementConfig")
    def put_custom_placement_config(
        self,
        *,
        data_locations: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param data_locations: The list of individual regions that comprise a dual-region bucket. See the docs for a list of acceptable regions. Note: If any of the data_locations changes, it will recreate the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#data_locations StorageBucket#data_locations}
        '''
        value = StorageBucketCustomPlacementConfig(data_locations=data_locations)

        return typing.cast(None, jsii.invoke(self, "putCustomPlacementConfig", [value]))

    @jsii.member(jsii_name="putEncryption")
    def put_encryption(self, *, default_kms_key_name: builtins.str) -> None:
        '''
        :param default_kms_key_name: A Cloud KMS key that will be used to encrypt objects inserted into this bucket, if no encryption method is specified. You must pay attention to whether the crypto key is available in the location that this bucket is created in. See the docs for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#default_kms_key_name StorageBucket#default_kms_key_name}
        '''
        value = StorageBucketEncryption(default_kms_key_name=default_kms_key_name)

        return typing.cast(None, jsii.invoke(self, "putEncryption", [value]))

    @jsii.member(jsii_name="putHierarchicalNamespace")
    def put_hierarchical_namespace(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Set this field true to organize bucket with logical file system structure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#enabled StorageBucket#enabled}
        '''
        value = StorageBucketHierarchicalNamespace(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putHierarchicalNamespace", [value]))

    @jsii.member(jsii_name="putIpFilter")
    def put_ip_filter(
        self,
        *,
        mode: builtins.str,
        allow_all_service_agent_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_cross_org_vpcs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_network_source: typing.Optional[typing.Union["StorageBucketIpFilterPublicNetworkSource", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_network_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageBucketIpFilterVpcNetworkSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param mode: The mode of the IP filter. Valid values are 'Enabled' and 'Disabled'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#mode StorageBucket#mode}
        :param allow_all_service_agent_access: Whether to allow all service agents to access the bucket regardless of the IP filter configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#allow_all_service_agent_access StorageBucket#allow_all_service_agent_access}
        :param allow_cross_org_vpcs: Whether to allow cross-org VPCs in the bucket's IP filter configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#allow_cross_org_vpcs StorageBucket#allow_cross_org_vpcs}
        :param public_network_source: public_network_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#public_network_source StorageBucket#public_network_source}
        :param vpc_network_sources: vpc_network_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#vpc_network_sources StorageBucket#vpc_network_sources}
        '''
        value = StorageBucketIpFilter(
            mode=mode,
            allow_all_service_agent_access=allow_all_service_agent_access,
            allow_cross_org_vpcs=allow_cross_org_vpcs,
            public_network_source=public_network_source,
            vpc_network_sources=vpc_network_sources,
        )

        return typing.cast(None, jsii.invoke(self, "putIpFilter", [value]))

    @jsii.member(jsii_name="putLifecycleRule")
    def put_lifecycle_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageBucketLifecycleRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da96ca771ca4518f7bd37937e25d1001a9749f636947aeed73553c8170141a8)
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
        :param log_bucket: The bucket that will receive log objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#log_bucket StorageBucket#log_bucket}
        :param log_object_prefix: The object prefix for log objects. If it's not provided, by default Google Cloud Storage sets this to this bucket's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#log_object_prefix StorageBucket#log_object_prefix}
        '''
        value = StorageBucketLogging(
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
        :param retention_period: The period of time, in seconds, that objects in the bucket must be retained and cannot be deleted, overwritten, or archived. The value must be less than 3,155,760,000 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#retention_period StorageBucket#retention_period}
        :param is_locked: If set to true, the bucket will be locked and permanently restrict edits to the bucket's retention policy. Caution: Locking a bucket is an irreversible action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#is_locked StorageBucket#is_locked}
        '''
        value = StorageBucketRetentionPolicy(
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
        :param retention_duration_seconds: The duration in seconds that soft-deleted objects in the bucket will be retained and cannot be permanently deleted. Default value is 604800. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#retention_duration_seconds StorageBucket#retention_duration_seconds}
        '''
        value = StorageBucketSoftDeletePolicy(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#create StorageBucket#create}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#read StorageBucket#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#update StorageBucket#update}.
        '''
        value = StorageBucketTimeouts(create=create, read=read, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVersioning")
    def put_versioning(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: While set to true, versioning is fully enabled for this bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#enabled StorageBucket#enabled}
        '''
        value = StorageBucketVersioning(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putVersioning", [value]))

    @jsii.member(jsii_name="putWebsite")
    def put_website(
        self,
        *,
        main_page_suffix: typing.Optional[builtins.str] = None,
        not_found_page: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param main_page_suffix: Behaves as the bucket's directory index where missing objects are treated as potential directories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#main_page_suffix StorageBucket#main_page_suffix}
        :param not_found_page: The custom object to return when a requested resource is not found. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#not_found_page StorageBucket#not_found_page}
        '''
        value = StorageBucketWebsite(
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
    def autoclass(self) -> "StorageBucketAutoclassOutputReference":
        return typing.cast("StorageBucketAutoclassOutputReference", jsii.get(self, "autoclass"))

    @builtins.property
    @jsii.member(jsii_name="cors")
    def cors(self) -> "StorageBucketCorsList":
        return typing.cast("StorageBucketCorsList", jsii.get(self, "cors"))

    @builtins.property
    @jsii.member(jsii_name="customPlacementConfig")
    def custom_placement_config(
        self,
    ) -> "StorageBucketCustomPlacementConfigOutputReference":
        return typing.cast("StorageBucketCustomPlacementConfigOutputReference", jsii.get(self, "customPlacementConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="encryption")
    def encryption(self) -> "StorageBucketEncryptionOutputReference":
        return typing.cast("StorageBucketEncryptionOutputReference", jsii.get(self, "encryption"))

    @builtins.property
    @jsii.member(jsii_name="hierarchicalNamespace")
    def hierarchical_namespace(
        self,
    ) -> "StorageBucketHierarchicalNamespaceOutputReference":
        return typing.cast("StorageBucketHierarchicalNamespaceOutputReference", jsii.get(self, "hierarchicalNamespace"))

    @builtins.property
    @jsii.member(jsii_name="ipFilter")
    def ip_filter(self) -> "StorageBucketIpFilterOutputReference":
        return typing.cast("StorageBucketIpFilterOutputReference", jsii.get(self, "ipFilter"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleRule")
    def lifecycle_rule(self) -> "StorageBucketLifecycleRuleList":
        return typing.cast("StorageBucketLifecycleRuleList", jsii.get(self, "lifecycleRule"))

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> "StorageBucketLoggingOutputReference":
        return typing.cast("StorageBucketLoggingOutputReference", jsii.get(self, "logging"))

    @builtins.property
    @jsii.member(jsii_name="projectNumber")
    def project_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "projectNumber"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(self) -> "StorageBucketRetentionPolicyOutputReference":
        return typing.cast("StorageBucketRetentionPolicyOutputReference", jsii.get(self, "retentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="softDeletePolicy")
    def soft_delete_policy(self) -> "StorageBucketSoftDeletePolicyOutputReference":
        return typing.cast("StorageBucketSoftDeletePolicyOutputReference", jsii.get(self, "softDeletePolicy"))

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
    def timeouts(self) -> "StorageBucketTimeoutsOutputReference":
        return typing.cast("StorageBucketTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def versioning(self) -> "StorageBucketVersioningOutputReference":
        return typing.cast("StorageBucketVersioningOutputReference", jsii.get(self, "versioning"))

    @builtins.property
    @jsii.member(jsii_name="website")
    def website(self) -> "StorageBucketWebsiteOutputReference":
        return typing.cast("StorageBucketWebsiteOutputReference", jsii.get(self, "website"))

    @builtins.property
    @jsii.member(jsii_name="autoclassInput")
    def autoclass_input(self) -> typing.Optional["StorageBucketAutoclass"]:
        return typing.cast(typing.Optional["StorageBucketAutoclass"], jsii.get(self, "autoclassInput"))

    @builtins.property
    @jsii.member(jsii_name="corsInput")
    def cors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageBucketCors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageBucketCors"]]], jsii.get(self, "corsInput"))

    @builtins.property
    @jsii.member(jsii_name="customPlacementConfigInput")
    def custom_placement_config_input(
        self,
    ) -> typing.Optional["StorageBucketCustomPlacementConfig"]:
        return typing.cast(typing.Optional["StorageBucketCustomPlacementConfig"], jsii.get(self, "customPlacementConfigInput"))

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
    def encryption_input(self) -> typing.Optional["StorageBucketEncryption"]:
        return typing.cast(typing.Optional["StorageBucketEncryption"], jsii.get(self, "encryptionInput"))

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
    ) -> typing.Optional["StorageBucketHierarchicalNamespace"]:
        return typing.cast(typing.Optional["StorageBucketHierarchicalNamespace"], jsii.get(self, "hierarchicalNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipFilterInput")
    def ip_filter_input(self) -> typing.Optional["StorageBucketIpFilter"]:
        return typing.cast(typing.Optional["StorageBucketIpFilter"], jsii.get(self, "ipFilterInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageBucketLifecycleRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageBucketLifecycleRule"]]], jsii.get(self, "lifecycleRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(self) -> typing.Optional["StorageBucketLogging"]:
        return typing.cast(typing.Optional["StorageBucketLogging"], jsii.get(self, "loggingInput"))

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
    def retention_policy_input(self) -> typing.Optional["StorageBucketRetentionPolicy"]:
        return typing.cast(typing.Optional["StorageBucketRetentionPolicy"], jsii.get(self, "retentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="rpoInput")
    def rpo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rpoInput"))

    @builtins.property
    @jsii.member(jsii_name="softDeletePolicyInput")
    def soft_delete_policy_input(
        self,
    ) -> typing.Optional["StorageBucketSoftDeletePolicy"]:
        return typing.cast(typing.Optional["StorageBucketSoftDeletePolicy"], jsii.get(self, "softDeletePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="storageClassInput")
    def storage_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageBucketTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageBucketTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="uniformBucketLevelAccessInput")
    def uniform_bucket_level_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "uniformBucketLevelAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="versioningInput")
    def versioning_input(self) -> typing.Optional["StorageBucketVersioning"]:
        return typing.cast(typing.Optional["StorageBucketVersioning"], jsii.get(self, "versioningInput"))

    @builtins.property
    @jsii.member(jsii_name="websiteInput")
    def website_input(self) -> typing.Optional["StorageBucketWebsite"]:
        return typing.cast(typing.Optional["StorageBucketWebsite"], jsii.get(self, "websiteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1c43eae756ecff4cd6f7b91f4ec11ed04440fcb71b243e49ce039c92ff6a9918)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e468f0387b1f9d2ffc8a55eebd5537c94e8b181f1cb1f446352f37e5baf4a0d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb61d63720b396050733ba0d6474dfdb4c573f93d7ddfb5b884d5b9b15b5b742)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd1893c8c094bb11bc262d072489042671436b8c3fe6cc3a481beed8205ec85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a89d7701039dfac2be115c33e5e95fa1010b55cffa2edaf96117b847110e334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91af7bcba55239c092d85914170cf06329955e61e9cb714f588fdcb4579d42b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b7353882c4f18e87609a1616df9e1f8d6861a51e07df819c80ea64fe976d367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4037405b9499b1438ec04e86ae0cdd4a0f8036b3f77ab7ad3254af55d3f4640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicAccessPrevention")
    def public_access_prevention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicAccessPrevention"))

    @public_access_prevention.setter
    def public_access_prevention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9db37c586455b1a77c043261511ab2c1467b9e14de30f8129304c312767aeaa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00a6d4447b1938cbba00fc73ebb836c6ec0a363a66ec9e642f96477929fc59f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requesterPays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rpo")
    def rpo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rpo"))

    @rpo.setter
    def rpo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__491beb0b40b7ffb57becd92dcb90591e292ea12e953393d6d13d516bc01845de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rpo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4ddcace566f24841caa5c561560251f9eaf34e7b5fc53ec165c1023d4be028)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e5e1e2b0f322395700141c6e81f5aad973f54de7b1b06f57b19c60c0ab00941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uniformBucketLevelAccess", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketAutoclass",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "terminal_storage_class": "terminalStorageClass",
    },
)
class StorageBucketAutoclass:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        terminal_storage_class: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: While set to true, autoclass automatically transitions objects in your bucket to appropriate storage classes based on each object's access pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#enabled StorageBucket#enabled}
        :param terminal_storage_class: The storage class that objects in the bucket eventually transition to if they are not read for a certain length of time. Supported values include: NEARLINE, ARCHIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#terminal_storage_class StorageBucket#terminal_storage_class}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8cff21a910b9b61ba752a0012d00077dae243fa135bfe26c4efbbfce20a1766)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#enabled StorageBucket#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def terminal_storage_class(self) -> typing.Optional[builtins.str]:
        '''The storage class that objects in the bucket eventually transition to if they are not read for a certain length of time.

        Supported values include: NEARLINE, ARCHIVE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#terminal_storage_class StorageBucket#terminal_storage_class}
        '''
        result = self._values.get("terminal_storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketAutoclass(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketAutoclassOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketAutoclassOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2a0996c9b00ca79d1b6ca5fe535ad5d859258806c52208f814a30efa4568172)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6b771d700f0a859e7980db8ea0ad41978ab16a5b9c08e23a2de523faaffac29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminalStorageClass")
    def terminal_storage_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terminalStorageClass"))

    @terminal_storage_class.setter
    def terminal_storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__907826594ff7810e451d09868e94345e2c74a71d4d19b3481126675d1c92cd51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminalStorageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBucketAutoclass]:
        return typing.cast(typing.Optional[StorageBucketAutoclass], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StorageBucketAutoclass]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__951b9f16ba08ae05418f2f1f9e25ff7a8a67e5f9c7682f645a0a9d485ec2e84e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketConfig",
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
class StorageBucketConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        autoclass: typing.Optional[typing.Union[StorageBucketAutoclass, typing.Dict[builtins.str, typing.Any]]] = None,
        cors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageBucketCors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_placement_config: typing.Optional[typing.Union["StorageBucketCustomPlacementConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_event_based_hold: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_object_retention: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption: typing.Optional[typing.Union["StorageBucketEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hierarchical_namespace: typing.Optional[typing.Union["StorageBucketHierarchicalNamespace", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_filter: typing.Optional[typing.Union["StorageBucketIpFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageBucketLifecycleRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        logging: typing.Optional[typing.Union["StorageBucketLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        public_access_prevention: typing.Optional[builtins.str] = None,
        requester_pays: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_policy: typing.Optional[typing.Union["StorageBucketRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        rpo: typing.Optional[builtins.str] = None,
        soft_delete_policy: typing.Optional[typing.Union["StorageBucketSoftDeletePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_class: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StorageBucketTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        uniform_bucket_level_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        versioning: typing.Optional[typing.Union["StorageBucketVersioning", typing.Dict[builtins.str, typing.Any]]] = None,
        website: typing.Optional[typing.Union["StorageBucketWebsite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The Google Cloud Storage location or region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#location StorageBucket#location}
        :param name: The name of the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#name StorageBucket#name}
        :param autoclass: autoclass block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#autoclass StorageBucket#autoclass}
        :param cors: cors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#cors StorageBucket#cors}
        :param custom_placement_config: custom_placement_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#custom_placement_config StorageBucket#custom_placement_config}
        :param default_event_based_hold: Whether or not to automatically apply an eventBasedHold to new objects added to the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#default_event_based_hold StorageBucket#default_event_based_hold}
        :param enable_object_retention: Enables each object in the bucket to have its own retention policy, which prevents deletion until stored for a specific length of time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#enable_object_retention StorageBucket#enable_object_retention}
        :param encryption: encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#encryption StorageBucket#encryption}
        :param force_destroy: When deleting a bucket, this boolean option will delete all contained objects, or anywhereCaches (if any). If you try to delete a bucket that contains objects or anywhereCaches, Terraform will fail that run, deleting anywhereCaches may take 80 minutes to complete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#force_destroy StorageBucket#force_destroy}
        :param hierarchical_namespace: hierarchical_namespace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#hierarchical_namespace StorageBucket#hierarchical_namespace}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#id StorageBucket#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_filter: ip_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#ip_filter StorageBucket#ip_filter}
        :param labels: A set of key/value label pairs to assign to the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#labels StorageBucket#labels}
        :param lifecycle_rule: lifecycle_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#lifecycle_rule StorageBucket#lifecycle_rule}
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#logging StorageBucket#logging}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#project StorageBucket#project}
        :param public_access_prevention: Prevents public access to a bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#public_access_prevention StorageBucket#public_access_prevention}
        :param requester_pays: Enables Requester Pays on a storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#requester_pays StorageBucket#requester_pays}
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#retention_policy StorageBucket#retention_policy}
        :param rpo: Specifies the RPO setting of bucket. If set 'ASYNC_TURBO', The Turbo Replication will be enabled for the dual-region bucket. Value 'DEFAULT' will set RPO setting to default. Turbo Replication is only for buckets in dual-regions.See the docs for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#rpo StorageBucket#rpo}
        :param soft_delete_policy: soft_delete_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#soft_delete_policy StorageBucket#soft_delete_policy}
        :param storage_class: The Storage Class of the new bucket. Supported values include: STANDARD, MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#storage_class StorageBucket#storage_class}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#timeouts StorageBucket#timeouts}
        :param uniform_bucket_level_access: Enables uniform bucket-level access on a bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#uniform_bucket_level_access StorageBucket#uniform_bucket_level_access}
        :param versioning: versioning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#versioning StorageBucket#versioning}
        :param website: website block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#website StorageBucket#website}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoclass, dict):
            autoclass = StorageBucketAutoclass(**autoclass)
        if isinstance(custom_placement_config, dict):
            custom_placement_config = StorageBucketCustomPlacementConfig(**custom_placement_config)
        if isinstance(encryption, dict):
            encryption = StorageBucketEncryption(**encryption)
        if isinstance(hierarchical_namespace, dict):
            hierarchical_namespace = StorageBucketHierarchicalNamespace(**hierarchical_namespace)
        if isinstance(ip_filter, dict):
            ip_filter = StorageBucketIpFilter(**ip_filter)
        if isinstance(logging, dict):
            logging = StorageBucketLogging(**logging)
        if isinstance(retention_policy, dict):
            retention_policy = StorageBucketRetentionPolicy(**retention_policy)
        if isinstance(soft_delete_policy, dict):
            soft_delete_policy = StorageBucketSoftDeletePolicy(**soft_delete_policy)
        if isinstance(timeouts, dict):
            timeouts = StorageBucketTimeouts(**timeouts)
        if isinstance(versioning, dict):
            versioning = StorageBucketVersioning(**versioning)
        if isinstance(website, dict):
            website = StorageBucketWebsite(**website)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d74d186ee8573d20d9bfd535070f237fc48472bb2a3bfe49962236f91ed4a86)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#location StorageBucket#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#name StorageBucket#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoclass(self) -> typing.Optional[StorageBucketAutoclass]:
        '''autoclass block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#autoclass StorageBucket#autoclass}
        '''
        result = self._values.get("autoclass")
        return typing.cast(typing.Optional[StorageBucketAutoclass], result)

    @builtins.property
    def cors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageBucketCors"]]]:
        '''cors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#cors StorageBucket#cors}
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageBucketCors"]]], result)

    @builtins.property
    def custom_placement_config(
        self,
    ) -> typing.Optional["StorageBucketCustomPlacementConfig"]:
        '''custom_placement_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#custom_placement_config StorageBucket#custom_placement_config}
        '''
        result = self._values.get("custom_placement_config")
        return typing.cast(typing.Optional["StorageBucketCustomPlacementConfig"], result)

    @builtins.property
    def default_event_based_hold(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not to automatically apply an eventBasedHold to new objects added to the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#default_event_based_hold StorageBucket#default_event_based_hold}
        '''
        result = self._values.get("default_event_based_hold")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_object_retention(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables each object in the bucket to have its own retention policy, which prevents deletion until stored for a specific length of time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#enable_object_retention StorageBucket#enable_object_retention}
        '''
        result = self._values.get("enable_object_retention")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption(self) -> typing.Optional["StorageBucketEncryption"]:
        '''encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#encryption StorageBucket#encryption}
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional["StorageBucketEncryption"], result)

    @builtins.property
    def force_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When deleting a bucket, this boolean option will delete all contained objects, or anywhereCaches (if any).

        If you try to delete a bucket that contains objects or anywhereCaches, Terraform will fail that run, deleting anywhereCaches may take 80 minutes to complete.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#force_destroy StorageBucket#force_destroy}
        '''
        result = self._values.get("force_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hierarchical_namespace(
        self,
    ) -> typing.Optional["StorageBucketHierarchicalNamespace"]:
        '''hierarchical_namespace block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#hierarchical_namespace StorageBucket#hierarchical_namespace}
        '''
        result = self._values.get("hierarchical_namespace")
        return typing.cast(typing.Optional["StorageBucketHierarchicalNamespace"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#id StorageBucket#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_filter(self) -> typing.Optional["StorageBucketIpFilter"]:
        '''ip_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#ip_filter StorageBucket#ip_filter}
        '''
        result = self._values.get("ip_filter")
        return typing.cast(typing.Optional["StorageBucketIpFilter"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#labels StorageBucket#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def lifecycle_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageBucketLifecycleRule"]]]:
        '''lifecycle_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#lifecycle_rule StorageBucket#lifecycle_rule}
        '''
        result = self._values.get("lifecycle_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageBucketLifecycleRule"]]], result)

    @builtins.property
    def logging(self) -> typing.Optional["StorageBucketLogging"]:
        '''logging block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#logging StorageBucket#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional["StorageBucketLogging"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#project StorageBucket#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_access_prevention(self) -> typing.Optional[builtins.str]:
        '''Prevents public access to a bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#public_access_prevention StorageBucket#public_access_prevention}
        '''
        result = self._values.get("public_access_prevention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requester_pays(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Requester Pays on a storage bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#requester_pays StorageBucket#requester_pays}
        '''
        result = self._values.get("requester_pays")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retention_policy(self) -> typing.Optional["StorageBucketRetentionPolicy"]:
        '''retention_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#retention_policy StorageBucket#retention_policy}
        '''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional["StorageBucketRetentionPolicy"], result)

    @builtins.property
    def rpo(self) -> typing.Optional[builtins.str]:
        '''Specifies the RPO setting of bucket.

        If set 'ASYNC_TURBO', The Turbo Replication will be enabled for the dual-region bucket. Value 'DEFAULT' will set RPO setting to default. Turbo Replication is only for buckets in dual-regions.See the docs for more details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#rpo StorageBucket#rpo}
        '''
        result = self._values.get("rpo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def soft_delete_policy(self) -> typing.Optional["StorageBucketSoftDeletePolicy"]:
        '''soft_delete_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#soft_delete_policy StorageBucket#soft_delete_policy}
        '''
        result = self._values.get("soft_delete_policy")
        return typing.cast(typing.Optional["StorageBucketSoftDeletePolicy"], result)

    @builtins.property
    def storage_class(self) -> typing.Optional[builtins.str]:
        '''The Storage Class of the new bucket. Supported values include: STANDARD, MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#storage_class StorageBucket#storage_class}
        '''
        result = self._values.get("storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["StorageBucketTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#timeouts StorageBucket#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["StorageBucketTimeouts"], result)

    @builtins.property
    def uniform_bucket_level_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables uniform bucket-level access on a bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#uniform_bucket_level_access StorageBucket#uniform_bucket_level_access}
        '''
        result = self._values.get("uniform_bucket_level_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def versioning(self) -> typing.Optional["StorageBucketVersioning"]:
        '''versioning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#versioning StorageBucket#versioning}
        '''
        result = self._values.get("versioning")
        return typing.cast(typing.Optional["StorageBucketVersioning"], result)

    @builtins.property
    def website(self) -> typing.Optional["StorageBucketWebsite"]:
        '''website block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#website StorageBucket#website}
        '''
        result = self._values.get("website")
        return typing.cast(typing.Optional["StorageBucketWebsite"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketCors",
    jsii_struct_bases=[],
    name_mapping={
        "max_age_seconds": "maxAgeSeconds",
        "method": "method",
        "origin": "origin",
        "response_header": "responseHeader",
    },
)
class StorageBucketCors:
    def __init__(
        self,
        *,
        max_age_seconds: typing.Optional[jsii.Number] = None,
        method: typing.Optional[typing.Sequence[builtins.str]] = None,
        origin: typing.Optional[typing.Sequence[builtins.str]] = None,
        response_header: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param max_age_seconds: The value, in seconds, to return in the Access-Control-Max-Age header used in preflight responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#max_age_seconds StorageBucket#max_age_seconds}
        :param method: The list of HTTP methods on which to include CORS response headers, (GET, OPTIONS, POST, etc) Note: "*" is permitted in the list of methods, and means "any method". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#method StorageBucket#method}
        :param origin: The list of Origins eligible to receive CORS response headers. Note: "*" is permitted in the list of origins, and means "any Origin". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#origin StorageBucket#origin}
        :param response_header: The list of HTTP headers other than the simple response headers to give permission for the user-agent to share across domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#response_header StorageBucket#response_header}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aef412622584f98b084b338d3d4617546429e4bcc4a1890188e397260f9aba4a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#max_age_seconds StorageBucket#max_age_seconds}
        '''
        result = self._values.get("max_age_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def method(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of HTTP methods on which to include CORS response headers, (GET, OPTIONS, POST, etc) Note: "*" is permitted in the list of methods, and means "any method".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#method StorageBucket#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def origin(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of Origins eligible to receive CORS response headers.

        Note: "*" is permitted in the list of origins, and means "any Origin".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#origin StorageBucket#origin}
        '''
        result = self._values.get("origin")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def response_header(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of HTTP headers other than the simple response headers to give permission for the user-agent to share across domains.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#response_header StorageBucket#response_header}
        '''
        result = self._values.get("response_header")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketCors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketCorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketCorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cfcc2af4509c613f0b10e3f70aadcc5f3a0ebab463d62e0a0afb8e836a6f4bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "StorageBucketCorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87342c5fc1eceafe645dca3d5f9649f12d0ce39fdc1560bafaf40351477e997c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageBucketCorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ff1d56728aed59557b642e045353d68e3ac8e645fd6de91e9e3aaba1dcd60ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32a7a46ae22349f98086db40b2983b977e28b17524513df307f2ab9ea9d8541a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dfa836c103a07baeef6370f36034b124c2133af8a1bd235ccf16c40d044f7e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageBucketCors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageBucketCors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageBucketCors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e642000d4f6bc88b80ff0fcfe61614a26781fae006c7ecf751010218b3a1b1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageBucketCorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketCorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e553d4ca7afc37244257225bdb272bdc0ca0be50eaa20607f38fa4418bf0dd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60d61147263d9216a83b53e00a4dfe23d4504b2d15581190498765bcd302efc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAgeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "method"))

    @method.setter
    def method(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e522e6664a079012e73adf2db5613f04b507880d59b39759b5e4ecb866b7957)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="origin")
    def origin(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "origin"))

    @origin.setter
    def origin(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__144757fefde1a67186bb8cc53b3d28ad2fe508315ca2650061df4aab039eac64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "origin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseHeader")
    def response_header(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "responseHeader"))

    @response_header.setter
    def response_header(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0a04672b1337fb5032a777e7133486ce1bb385206be806e262101be750b6af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketCors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketCors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketCors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a600eaa092abd30a72b58b4f40707250019b798aed12c136d7d7159c2959879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketCustomPlacementConfig",
    jsii_struct_bases=[],
    name_mapping={"data_locations": "dataLocations"},
)
class StorageBucketCustomPlacementConfig:
    def __init__(self, *, data_locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param data_locations: The list of individual regions that comprise a dual-region bucket. See the docs for a list of acceptable regions. Note: If any of the data_locations changes, it will recreate the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#data_locations StorageBucket#data_locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be966fd842cb3b190260f703dc8f02f24e359b7144512e40d5c3088035f70986)
            check_type(argname="argument data_locations", value=data_locations, expected_type=type_hints["data_locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_locations": data_locations,
        }

    @builtins.property
    def data_locations(self) -> typing.List[builtins.str]:
        '''The list of individual regions that comprise a dual-region bucket.

        See the docs for a list of acceptable regions. Note: If any of the data_locations changes, it will recreate the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#data_locations StorageBucket#data_locations}
        '''
        result = self._values.get("data_locations")
        assert result is not None, "Required property 'data_locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketCustomPlacementConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketCustomPlacementConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketCustomPlacementConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26ad3e3a6fc39e25d0056c473a974a0afd47b0386d0509a051938a7ca65038c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fdc904692d400a50c3c578a54d5dfc009a743132db1077e9070763a45ab5ece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataLocations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBucketCustomPlacementConfig]:
        return typing.cast(typing.Optional[StorageBucketCustomPlacementConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageBucketCustomPlacementConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0382ea66a6b6cda39c04ed4b095e7cdc2dad4c41493ff7af5d9fbe1875818d15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketEncryption",
    jsii_struct_bases=[],
    name_mapping={"default_kms_key_name": "defaultKmsKeyName"},
)
class StorageBucketEncryption:
    def __init__(self, *, default_kms_key_name: builtins.str) -> None:
        '''
        :param default_kms_key_name: A Cloud KMS key that will be used to encrypt objects inserted into this bucket, if no encryption method is specified. You must pay attention to whether the crypto key is available in the location that this bucket is created in. See the docs for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#default_kms_key_name StorageBucket#default_kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__233e32da1f81399aa3046393c53d55c23ba834bd7e142ddaae4c88fcf80886d9)
            check_type(argname="argument default_kms_key_name", value=default_kms_key_name, expected_type=type_hints["default_kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_kms_key_name": default_kms_key_name,
        }

    @builtins.property
    def default_kms_key_name(self) -> builtins.str:
        '''A Cloud KMS key that will be used to encrypt objects inserted into this bucket, if no encryption method is specified.

        You must pay attention to whether the crypto key is available in the location that this bucket is created in. See the docs for more details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#default_kms_key_name StorageBucket#default_kms_key_name}
        '''
        result = self._values.get("default_kms_key_name")
        assert result is not None, "Required property 'default_kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__340fbc3369a5aafd0152aac7fbd7d02e51f180e0e9ac85883ad535e1dea8ff3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f291091cc3ace1ba31cca014095424910b8b7b26bacc254f1cd651c6a0f500d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultKmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBucketEncryption]:
        return typing.cast(typing.Optional[StorageBucketEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StorageBucketEncryption]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a98d7b1c0bdc44a0990d33673e6a105f06939fc121f9b133721afe806a8da1ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketHierarchicalNamespace",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class StorageBucketHierarchicalNamespace:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Set this field true to organize bucket with logical file system structure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#enabled StorageBucket#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834d242bb36366b1c04219c3bdc78f160e0d2100216e4daca2cb83178c4f28e4)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Set this field true to organize bucket with logical file system structure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#enabled StorageBucket#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketHierarchicalNamespace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketHierarchicalNamespaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketHierarchicalNamespaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1a8e6eb37407b8d2a9a3afb876a45d0843fb990c976d7c473649c597077ebfc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c72aa09511f5736841d9055cd338dc6b6762d3c1894e3610af17696efe849990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBucketHierarchicalNamespace]:
        return typing.cast(typing.Optional[StorageBucketHierarchicalNamespace], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageBucketHierarchicalNamespace],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf3789277a693f3407b19afe162ba91723e0ddb5fdd01996c025b83f89eed6cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketIpFilter",
    jsii_struct_bases=[],
    name_mapping={
        "mode": "mode",
        "allow_all_service_agent_access": "allowAllServiceAgentAccess",
        "allow_cross_org_vpcs": "allowCrossOrgVpcs",
        "public_network_source": "publicNetworkSource",
        "vpc_network_sources": "vpcNetworkSources",
    },
)
class StorageBucketIpFilter:
    def __init__(
        self,
        *,
        mode: builtins.str,
        allow_all_service_agent_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_cross_org_vpcs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_network_source: typing.Optional[typing.Union["StorageBucketIpFilterPublicNetworkSource", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_network_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageBucketIpFilterVpcNetworkSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param mode: The mode of the IP filter. Valid values are 'Enabled' and 'Disabled'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#mode StorageBucket#mode}
        :param allow_all_service_agent_access: Whether to allow all service agents to access the bucket regardless of the IP filter configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#allow_all_service_agent_access StorageBucket#allow_all_service_agent_access}
        :param allow_cross_org_vpcs: Whether to allow cross-org VPCs in the bucket's IP filter configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#allow_cross_org_vpcs StorageBucket#allow_cross_org_vpcs}
        :param public_network_source: public_network_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#public_network_source StorageBucket#public_network_source}
        :param vpc_network_sources: vpc_network_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#vpc_network_sources StorageBucket#vpc_network_sources}
        '''
        if isinstance(public_network_source, dict):
            public_network_source = StorageBucketIpFilterPublicNetworkSource(**public_network_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d460705e4a65c23dc8c2700f96b8f966196387db9ccfaa23bb1ca526355227)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument allow_all_service_agent_access", value=allow_all_service_agent_access, expected_type=type_hints["allow_all_service_agent_access"])
            check_type(argname="argument allow_cross_org_vpcs", value=allow_cross_org_vpcs, expected_type=type_hints["allow_cross_org_vpcs"])
            check_type(argname="argument public_network_source", value=public_network_source, expected_type=type_hints["public_network_source"])
            check_type(argname="argument vpc_network_sources", value=vpc_network_sources, expected_type=type_hints["vpc_network_sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if allow_all_service_agent_access is not None:
            self._values["allow_all_service_agent_access"] = allow_all_service_agent_access
        if allow_cross_org_vpcs is not None:
            self._values["allow_cross_org_vpcs"] = allow_cross_org_vpcs
        if public_network_source is not None:
            self._values["public_network_source"] = public_network_source
        if vpc_network_sources is not None:
            self._values["vpc_network_sources"] = vpc_network_sources

    @builtins.property
    def mode(self) -> builtins.str:
        '''The mode of the IP filter. Valid values are 'Enabled' and 'Disabled'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#mode StorageBucket#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_all_service_agent_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow all service agents to access the bucket regardless of the IP filter configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#allow_all_service_agent_access StorageBucket#allow_all_service_agent_access}
        '''
        result = self._values.get("allow_all_service_agent_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_cross_org_vpcs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow cross-org VPCs in the bucket's IP filter configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#allow_cross_org_vpcs StorageBucket#allow_cross_org_vpcs}
        '''
        result = self._values.get("allow_cross_org_vpcs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def public_network_source(
        self,
    ) -> typing.Optional["StorageBucketIpFilterPublicNetworkSource"]:
        '''public_network_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#public_network_source StorageBucket#public_network_source}
        '''
        result = self._values.get("public_network_source")
        return typing.cast(typing.Optional["StorageBucketIpFilterPublicNetworkSource"], result)

    @builtins.property
    def vpc_network_sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageBucketIpFilterVpcNetworkSources"]]]:
        '''vpc_network_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#vpc_network_sources StorageBucket#vpc_network_sources}
        '''
        result = self._values.get("vpc_network_sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageBucketIpFilterVpcNetworkSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketIpFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketIpFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketIpFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08449c4c0934b6fdc895db577a9d99ed00ee6827254e7a726ddb35c9babbbc1a)
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
        :param allowed_ip_cidr_ranges: The list of public IPv4, IPv6 cidr ranges that are allowed to access the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#allowed_ip_cidr_ranges StorageBucket#allowed_ip_cidr_ranges}
        '''
        value = StorageBucketIpFilterPublicNetworkSource(
            allowed_ip_cidr_ranges=allowed_ip_cidr_ranges
        )

        return typing.cast(None, jsii.invoke(self, "putPublicNetworkSource", [value]))

    @jsii.member(jsii_name="putVpcNetworkSources")
    def put_vpc_network_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageBucketIpFilterVpcNetworkSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a327456067142a12ab41851fd18290bb589aec2dcc41643822e4cc84d9124c3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVpcNetworkSources", [value]))

    @jsii.member(jsii_name="resetAllowAllServiceAgentAccess")
    def reset_allow_all_service_agent_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAllServiceAgentAccess", []))

    @jsii.member(jsii_name="resetAllowCrossOrgVpcs")
    def reset_allow_cross_org_vpcs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowCrossOrgVpcs", []))

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
    ) -> "StorageBucketIpFilterPublicNetworkSourceOutputReference":
        return typing.cast("StorageBucketIpFilterPublicNetworkSourceOutputReference", jsii.get(self, "publicNetworkSource"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetworkSources")
    def vpc_network_sources(self) -> "StorageBucketIpFilterVpcNetworkSourcesList":
        return typing.cast("StorageBucketIpFilterVpcNetworkSourcesList", jsii.get(self, "vpcNetworkSources"))

    @builtins.property
    @jsii.member(jsii_name="allowAllServiceAgentAccessInput")
    def allow_all_service_agent_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAllServiceAgentAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="allowCrossOrgVpcsInput")
    def allow_cross_org_vpcs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowCrossOrgVpcsInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkSourceInput")
    def public_network_source_input(
        self,
    ) -> typing.Optional["StorageBucketIpFilterPublicNetworkSource"]:
        return typing.cast(typing.Optional["StorageBucketIpFilterPublicNetworkSource"], jsii.get(self, "publicNetworkSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetworkSourcesInput")
    def vpc_network_sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageBucketIpFilterVpcNetworkSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageBucketIpFilterVpcNetworkSources"]]], jsii.get(self, "vpcNetworkSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAllServiceAgentAccess")
    def allow_all_service_agent_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAllServiceAgentAccess"))

    @allow_all_service_agent_access.setter
    def allow_all_service_agent_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b6b5b7c68cf5c312ac1816c7e79cbdef70007c25e00d2ca1569bf4acd40986e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAllServiceAgentAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowCrossOrgVpcs")
    def allow_cross_org_vpcs(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowCrossOrgVpcs"))

    @allow_cross_org_vpcs.setter
    def allow_cross_org_vpcs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dfdc2e59c0c0a3ac5d0014c957869d1ae820237fcf972123a90e8eb177efe7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowCrossOrgVpcs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530e56480d5fa9ef176b6f6a4f67f4bd7b3282ee984973412dd7425b6090f22c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBucketIpFilter]:
        return typing.cast(typing.Optional[StorageBucketIpFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StorageBucketIpFilter]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5dd3d2a000301a5325dd57784e7eaf1af697ba09cb88c680c44a8aa5c7207de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketIpFilterPublicNetworkSource",
    jsii_struct_bases=[],
    name_mapping={"allowed_ip_cidr_ranges": "allowedIpCidrRanges"},
)
class StorageBucketIpFilterPublicNetworkSource:
    def __init__(
        self,
        *,
        allowed_ip_cidr_ranges: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param allowed_ip_cidr_ranges: The list of public IPv4, IPv6 cidr ranges that are allowed to access the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#allowed_ip_cidr_ranges StorageBucket#allowed_ip_cidr_ranges}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177a019124eed5ee07ad95775b50cf2f7c68a20c219e00f61cb5bb223f67b683)
            check_type(argname="argument allowed_ip_cidr_ranges", value=allowed_ip_cidr_ranges, expected_type=type_hints["allowed_ip_cidr_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_ip_cidr_ranges": allowed_ip_cidr_ranges,
        }

    @builtins.property
    def allowed_ip_cidr_ranges(self) -> typing.List[builtins.str]:
        '''The list of public IPv4, IPv6 cidr ranges that are allowed to access the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#allowed_ip_cidr_ranges StorageBucket#allowed_ip_cidr_ranges}
        '''
        result = self._values.get("allowed_ip_cidr_ranges")
        assert result is not None, "Required property 'allowed_ip_cidr_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketIpFilterPublicNetworkSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketIpFilterPublicNetworkSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketIpFilterPublicNetworkSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cacd93b8395869e6eeaeed91f814b4b24754a25210c8129e826f784ad15b988)
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
            type_hints = typing.get_type_hints(_typecheckingstub__513070bc23da80eff4a4e3af151fb9688bfd3b85aaea9ed94f3ec902abc7d84f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedIpCidrRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageBucketIpFilterPublicNetworkSource]:
        return typing.cast(typing.Optional[StorageBucketIpFilterPublicNetworkSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageBucketIpFilterPublicNetworkSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68958f8db9ff009b64bbdec93229804a1d5c6709f8468eff485a0eb0c731b91f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketIpFilterVpcNetworkSources",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_ip_cidr_ranges": "allowedIpCidrRanges",
        "network": "network",
    },
)
class StorageBucketIpFilterVpcNetworkSources:
    def __init__(
        self,
        *,
        allowed_ip_cidr_ranges: typing.Sequence[builtins.str],
        network: builtins.str,
    ) -> None:
        '''
        :param allowed_ip_cidr_ranges: The list of public or private IPv4 and IPv6 CIDR ranges that can access the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#allowed_ip_cidr_ranges StorageBucket#allowed_ip_cidr_ranges}
        :param network: Name of the network. Format: projects/{PROJECT_ID}/global/networks/{NETWORK_NAME}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#network StorageBucket#network}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf796e130e66a1873a80b2dec977096bd0536550632f744cd324991bfd49732c)
            check_type(argname="argument allowed_ip_cidr_ranges", value=allowed_ip_cidr_ranges, expected_type=type_hints["allowed_ip_cidr_ranges"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_ip_cidr_ranges": allowed_ip_cidr_ranges,
            "network": network,
        }

    @builtins.property
    def allowed_ip_cidr_ranges(self) -> typing.List[builtins.str]:
        '''The list of public or private IPv4 and IPv6 CIDR ranges that can access the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#allowed_ip_cidr_ranges StorageBucket#allowed_ip_cidr_ranges}
        '''
        result = self._values.get("allowed_ip_cidr_ranges")
        assert result is not None, "Required property 'allowed_ip_cidr_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def network(self) -> builtins.str:
        '''Name of the network. Format: projects/{PROJECT_ID}/global/networks/{NETWORK_NAME}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#network StorageBucket#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketIpFilterVpcNetworkSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketIpFilterVpcNetworkSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketIpFilterVpcNetworkSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54adb5a6b6fe6e5fb87b81c0eea75dba9afb3b9bf7117abece9fc4a766723c3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageBucketIpFilterVpcNetworkSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b99843ae8fc252bf83329cd8eea873083afff226fefbd8902e756e86eeaeb8a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageBucketIpFilterVpcNetworkSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fcba357f3fd98ce7a87ff977eb73da5838e6e60b54fe2218f46ae0dd2d3e8e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c43dbc33a3b31bfe88bec371944217fbe182fd0a80a44cd7182cd719a639ff8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__831499a9c03ee051b40151ec4e24674fdd944cb1f18a00a9ef233b7e9477ae00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageBucketIpFilterVpcNetworkSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageBucketIpFilterVpcNetworkSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageBucketIpFilterVpcNetworkSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc7812cc02ac4f14682abe4f17ea3fa8ffcbfe235133038787c6625b744f1f42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageBucketIpFilterVpcNetworkSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketIpFilterVpcNetworkSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4eb0563c7860bdbf7976687809c06bd5e140a2162f964a9d75b3cd885259c4ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cffb0861b7dc0b0a2bca8ececd0f1f8b58783c6ee6d01d49c18d5f0922847ee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedIpCidrRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e2624b6c9bdf526c1493778734969b25b6a9915e7a47f2ac35df7e1f58cedf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketIpFilterVpcNetworkSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketIpFilterVpcNetworkSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketIpFilterVpcNetworkSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a238df146cbcec9d3e14555b8ec1e430793cd98ef21a9d477a76e6c4a4a34b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketLifecycleRule",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "condition": "condition"},
)
class StorageBucketLifecycleRule:
    def __init__(
        self,
        *,
        action: typing.Union["StorageBucketLifecycleRuleAction", typing.Dict[builtins.str, typing.Any]],
        condition: typing.Union["StorageBucketLifecycleRuleCondition", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#action StorageBucket#action}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#condition StorageBucket#condition}
        '''
        if isinstance(action, dict):
            action = StorageBucketLifecycleRuleAction(**action)
        if isinstance(condition, dict):
            condition = StorageBucketLifecycleRuleCondition(**condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58a152ae184b9c2f7237dcc670223a18cc3f24e301b4fb3a4664c4c1a00365a)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "condition": condition,
        }

    @builtins.property
    def action(self) -> "StorageBucketLifecycleRuleAction":
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#action StorageBucket#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("StorageBucketLifecycleRuleAction", result)

    @builtins.property
    def condition(self) -> "StorageBucketLifecycleRuleCondition":
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#condition StorageBucket#condition}
        '''
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast("StorageBucketLifecycleRuleCondition", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketLifecycleRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketLifecycleRuleAction",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "storage_class": "storageClass"},
)
class StorageBucketLifecycleRuleAction:
    def __init__(
        self,
        *,
        type: builtins.str,
        storage_class: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: The type of the action of this Lifecycle Rule. Supported values include: Delete, SetStorageClass and AbortIncompleteMultipartUpload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#type StorageBucket#type}
        :param storage_class: The target Storage Class of objects affected by this Lifecycle Rule. Supported values include: MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#storage_class StorageBucket#storage_class}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d9ff233c9198bbe2da4e903fe40cf1bf2aedfb779151f8b920f57a701d6a0dd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#type StorageBucket#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_class(self) -> typing.Optional[builtins.str]:
        '''The target Storage Class of objects affected by this Lifecycle Rule. Supported values include: MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#storage_class StorageBucket#storage_class}
        '''
        result = self._values.get("storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketLifecycleRuleAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketLifecycleRuleActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketLifecycleRuleActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__311817abe6861caf53cb3e32d8c7b0152aed06fa168d6aea74d60946b749a1aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20e3164cc155286ccc974c1a71dcf811c76f00cdc880e94494c7663ad2f3a267)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dfef90eeb6ce020a96dc2f0e2413d379d62df49c658849f9f680595e362b8e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBucketLifecycleRuleAction]:
        return typing.cast(typing.Optional[StorageBucketLifecycleRuleAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageBucketLifecycleRuleAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7573ff92eefa7bcc68024c6038b20bb839ccd158b3c892871c996cfedf49cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketLifecycleRuleCondition",
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
class StorageBucketLifecycleRuleCondition:
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
        :param age: Minimum age of an object in days to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#age StorageBucket#age}
        :param created_before: Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#created_before StorageBucket#created_before}
        :param custom_time_before: Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#custom_time_before StorageBucket#custom_time_before}
        :param days_since_custom_time: Number of days elapsed since the user-specified timestamp set on an object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#days_since_custom_time StorageBucket#days_since_custom_time}
        :param days_since_noncurrent_time: Number of days elapsed since the noncurrent timestamp of an object. This condition is relevant only for versioned objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#days_since_noncurrent_time StorageBucket#days_since_noncurrent_time}
        :param matches_prefix: One or more matching name prefixes to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#matches_prefix StorageBucket#matches_prefix}
        :param matches_storage_class: Storage Class of objects to satisfy this condition. Supported values include: MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE, STANDARD, DURABLE_REDUCED_AVAILABILITY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#matches_storage_class StorageBucket#matches_storage_class}
        :param matches_suffix: One or more matching name suffixes to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#matches_suffix StorageBucket#matches_suffix}
        :param noncurrent_time_before: Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#noncurrent_time_before StorageBucket#noncurrent_time_before}
        :param num_newer_versions: Relevant only for versioned objects. The number of newer versions of an object to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#num_newer_versions StorageBucket#num_newer_versions}
        :param send_age_if_zero: While set true, age value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the age field. It can be used alone or together with age. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#send_age_if_zero StorageBucket#send_age_if_zero}
        :param send_days_since_custom_time_if_zero: While set true, days_since_custom_time value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the days_since_custom_time field. It can be used alone or together with days_since_custom_time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#send_days_since_custom_time_if_zero StorageBucket#send_days_since_custom_time_if_zero}
        :param send_days_since_noncurrent_time_if_zero: While set true, days_since_noncurrent_time value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the days_since_noncurrent_time field. It can be used alone or together with days_since_noncurrent_time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#send_days_since_noncurrent_time_if_zero StorageBucket#send_days_since_noncurrent_time_if_zero}
        :param send_num_newer_versions_if_zero: While set true, num_newer_versions value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the num_newer_versions field. It can be used alone or together with num_newer_versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#send_num_newer_versions_if_zero StorageBucket#send_num_newer_versions_if_zero}
        :param with_state: Match to live and/or archived objects. Unversioned buckets have only live objects. Supported values include: "LIVE", "ARCHIVED", "ANY". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#with_state StorageBucket#with_state}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8aac0cdf7077b6114d49ee6654a4780e1eddc86fc3a941ab4cd9acaae68ba4b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#age StorageBucket#age}
        '''
        result = self._values.get("age")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def created_before(self) -> typing.Optional[builtins.str]:
        '''Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#created_before StorageBucket#created_before}
        '''
        result = self._values.get("created_before")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_time_before(self) -> typing.Optional[builtins.str]:
        '''Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#custom_time_before StorageBucket#custom_time_before}
        '''
        result = self._values.get("custom_time_before")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def days_since_custom_time(self) -> typing.Optional[jsii.Number]:
        '''Number of days elapsed since the user-specified timestamp set on an object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#days_since_custom_time StorageBucket#days_since_custom_time}
        '''
        result = self._values.get("days_since_custom_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def days_since_noncurrent_time(self) -> typing.Optional[jsii.Number]:
        '''Number of days elapsed since the noncurrent timestamp of an object. This 										condition is relevant only for versioned objects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#days_since_noncurrent_time StorageBucket#days_since_noncurrent_time}
        '''
        result = self._values.get("days_since_noncurrent_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def matches_prefix(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more matching name prefixes to satisfy this condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#matches_prefix StorageBucket#matches_prefix}
        '''
        result = self._values.get("matches_prefix")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def matches_storage_class(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Storage Class of objects to satisfy this condition. Supported values include: MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE, STANDARD, DURABLE_REDUCED_AVAILABILITY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#matches_storage_class StorageBucket#matches_storage_class}
        '''
        result = self._values.get("matches_storage_class")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def matches_suffix(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more matching name suffixes to satisfy this condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#matches_suffix StorageBucket#matches_suffix}
        '''
        result = self._values.get("matches_suffix")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def noncurrent_time_before(self) -> typing.Optional[builtins.str]:
        '''Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#noncurrent_time_before StorageBucket#noncurrent_time_before}
        '''
        result = self._values.get("noncurrent_time_before")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_newer_versions(self) -> typing.Optional[jsii.Number]:
        '''Relevant only for versioned objects. The number of newer versions of an object to satisfy this condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#num_newer_versions StorageBucket#num_newer_versions}
        '''
        result = self._values.get("num_newer_versions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def send_age_if_zero(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''While set true, age value will be sent in the request even for zero value of the field.

        This field is only useful for setting 0 value to the age field. It can be used alone or together with age.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#send_age_if_zero StorageBucket#send_age_if_zero}
        '''
        result = self._values.get("send_age_if_zero")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_days_since_custom_time_if_zero(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''While set true, days_since_custom_time value will be sent in the request even for zero value of the field.

        This field is only useful for setting 0 value to the days_since_custom_time field. It can be used alone or together with days_since_custom_time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#send_days_since_custom_time_if_zero StorageBucket#send_days_since_custom_time_if_zero}
        '''
        result = self._values.get("send_days_since_custom_time_if_zero")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_days_since_noncurrent_time_if_zero(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''While set true, days_since_noncurrent_time value will be sent in the request even for zero value of the field.

        This field is only useful for setting 0 value to the days_since_noncurrent_time field. It can be used alone or together with days_since_noncurrent_time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#send_days_since_noncurrent_time_if_zero StorageBucket#send_days_since_noncurrent_time_if_zero}
        '''
        result = self._values.get("send_days_since_noncurrent_time_if_zero")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_num_newer_versions_if_zero(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''While set true, num_newer_versions value will be sent in the request even for zero value of the field.

        This field is only useful for setting 0 value to the num_newer_versions field. It can be used alone or together with num_newer_versions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#send_num_newer_versions_if_zero StorageBucket#send_num_newer_versions_if_zero}
        '''
        result = self._values.get("send_num_newer_versions_if_zero")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def with_state(self) -> typing.Optional[builtins.str]:
        '''Match to live and/or archived objects. Unversioned buckets have only live objects. Supported values include: "LIVE", "ARCHIVED", "ANY".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#with_state StorageBucket#with_state}
        '''
        result = self._values.get("with_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketLifecycleRuleCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketLifecycleRuleConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketLifecycleRuleConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__433dcac421ee8e506852b692e5e2e8518f8b59710ee1b615e5915c3693c90f67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce4f4538fcd5caf334758699f364936b69b0718a2814ed82a0d997de6e7b6b0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "age", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createdBefore")
    def created_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdBefore"))

    @created_before.setter
    def created_before(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09458f9213df6b0229026994cd1bf98da0e7fa3a7f21458fbcf88f7fc0b742dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customTimeBefore")
    def custom_time_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customTimeBefore"))

    @custom_time_before.setter
    def custom_time_before(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aae13f8132abf7ff829d8f7f58fcf3a9f6aae86eb329e361ed73b19d003f05e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customTimeBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="daysSinceCustomTime")
    def days_since_custom_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "daysSinceCustomTime"))

    @days_since_custom_time.setter
    def days_since_custom_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__946735d8eeb03e951d3da5911efe846cfd9e35cf45ea881c3d8b9fcdc095fca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysSinceCustomTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="daysSinceNoncurrentTime")
    def days_since_noncurrent_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "daysSinceNoncurrentTime"))

    @days_since_noncurrent_time.setter
    def days_since_noncurrent_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff770efd8bd5a9d3d470c48d8a135842abc97eaa37ff0602a6cce6edab2281c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysSinceNoncurrentTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchesPrefix")
    def matches_prefix(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchesPrefix"))

    @matches_prefix.setter
    def matches_prefix(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec996d21b3decc6970a8c7b526726122c3c7e65b0ff79c77d1328eb9de5c2dcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchesPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchesStorageClass")
    def matches_storage_class(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchesStorageClass"))

    @matches_storage_class.setter
    def matches_storage_class(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa245f7ab118cc55d517bf2e6cafb0ea179140da3a5f5a6138d6efd75dd8b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchesStorageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchesSuffix")
    def matches_suffix(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchesSuffix"))

    @matches_suffix.setter
    def matches_suffix(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7cef68a55671fced4f273265a81e741c86e32931f8335f710f109f62f71f402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchesSuffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noncurrentTimeBefore")
    def noncurrent_time_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "noncurrentTimeBefore"))

    @noncurrent_time_before.setter
    def noncurrent_time_before(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33414a496a8714c1985c8193612e3616a030265b21b74a4213909bbe3813b8d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noncurrentTimeBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numNewerVersions")
    def num_newer_versions(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numNewerVersions"))

    @num_newer_versions.setter
    def num_newer_versions(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101480b6bafc9e0d78fec9df6a083de7172cfdd584dd3b0eb2e2382af1163bf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86351a822e237a41c07ddbc2026cbff51f8fa2a90b4587d2a8ca3dd0cdfe4ac8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cc82e1e252781474046be8c851efc6f69bf0481bdf8ab512cbad7633b14931e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe8291f3ab90ed5ba81d64b4147556a8c50837815fdbd060568aa99eebe313a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__297151f9e680026d033e09dc565d655dd7ced014f0fd0f82c04e359597ee9df7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendNumNewerVersionsIfZero", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withState")
    def with_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "withState"))

    @with_state.setter
    def with_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__956645a973c9f0a2bffa09a4bd836443f13726b42b4f0a3aca5e5245da2d7d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBucketLifecycleRuleCondition]:
        return typing.cast(typing.Optional[StorageBucketLifecycleRuleCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageBucketLifecycleRuleCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0225d3a07e1cc7fa6c2b92d84bef5d792c0e14f70d0d3118cd25e3b2356d7e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageBucketLifecycleRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketLifecycleRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eca3a82a285a501ba71ce714a649e353bec15a214806168c70930075d9da71ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "StorageBucketLifecycleRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__049b0a552d3f0a3efc1581a9ba89ad62335ffbdb5ef06a18a720621f2b2c6f46)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageBucketLifecycleRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a735e43291c656843d100e80270a3141ed7cb08802ff45180947adcfde0af5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7989d0a997476734a09ff95644a9ecbc9d43b1df22d91bee5c43e9b7e96b591d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cf43a2da1ff5823dbab67dcce6453b26fb42e3d93f29efcf75c3d066b53208e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageBucketLifecycleRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageBucketLifecycleRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageBucketLifecycleRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4403f4133b4cddfbc3dd149dd930a3478130a3a984672a74c7f17240ada7b333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageBucketLifecycleRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketLifecycleRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3088596f13a0abc5f8c56446774236ffc218168da2c83899637d28af1501988f)
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
        :param type: The type of the action of this Lifecycle Rule. Supported values include: Delete, SetStorageClass and AbortIncompleteMultipartUpload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#type StorageBucket#type}
        :param storage_class: The target Storage Class of objects affected by this Lifecycle Rule. Supported values include: MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#storage_class StorageBucket#storage_class}
        '''
        value = StorageBucketLifecycleRuleAction(
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
        :param age: Minimum age of an object in days to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#age StorageBucket#age}
        :param created_before: Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#created_before StorageBucket#created_before}
        :param custom_time_before: Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#custom_time_before StorageBucket#custom_time_before}
        :param days_since_custom_time: Number of days elapsed since the user-specified timestamp set on an object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#days_since_custom_time StorageBucket#days_since_custom_time}
        :param days_since_noncurrent_time: Number of days elapsed since the noncurrent timestamp of an object. This condition is relevant only for versioned objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#days_since_noncurrent_time StorageBucket#days_since_noncurrent_time}
        :param matches_prefix: One or more matching name prefixes to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#matches_prefix StorageBucket#matches_prefix}
        :param matches_storage_class: Storage Class of objects to satisfy this condition. Supported values include: MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE, STANDARD, DURABLE_REDUCED_AVAILABILITY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#matches_storage_class StorageBucket#matches_storage_class}
        :param matches_suffix: One or more matching name suffixes to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#matches_suffix StorageBucket#matches_suffix}
        :param noncurrent_time_before: Creation date of an object in RFC 3339 (e.g. 2017-06-13) to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#noncurrent_time_before StorageBucket#noncurrent_time_before}
        :param num_newer_versions: Relevant only for versioned objects. The number of newer versions of an object to satisfy this condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#num_newer_versions StorageBucket#num_newer_versions}
        :param send_age_if_zero: While set true, age value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the age field. It can be used alone or together with age. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#send_age_if_zero StorageBucket#send_age_if_zero}
        :param send_days_since_custom_time_if_zero: While set true, days_since_custom_time value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the days_since_custom_time field. It can be used alone or together with days_since_custom_time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#send_days_since_custom_time_if_zero StorageBucket#send_days_since_custom_time_if_zero}
        :param send_days_since_noncurrent_time_if_zero: While set true, days_since_noncurrent_time value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the days_since_noncurrent_time field. It can be used alone or together with days_since_noncurrent_time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#send_days_since_noncurrent_time_if_zero StorageBucket#send_days_since_noncurrent_time_if_zero}
        :param send_num_newer_versions_if_zero: While set true, num_newer_versions value will be sent in the request even for zero value of the field. This field is only useful for setting 0 value to the num_newer_versions field. It can be used alone or together with num_newer_versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#send_num_newer_versions_if_zero StorageBucket#send_num_newer_versions_if_zero}
        :param with_state: Match to live and/or archived objects. Unversioned buckets have only live objects. Supported values include: "LIVE", "ARCHIVED", "ANY". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#with_state StorageBucket#with_state}
        '''
        value = StorageBucketLifecycleRuleCondition(
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
    def action(self) -> StorageBucketLifecycleRuleActionOutputReference:
        return typing.cast(StorageBucketLifecycleRuleActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> StorageBucketLifecycleRuleConditionOutputReference:
        return typing.cast(StorageBucketLifecycleRuleConditionOutputReference, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[StorageBucketLifecycleRuleAction]:
        return typing.cast(typing.Optional[StorageBucketLifecycleRuleAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[StorageBucketLifecycleRuleCondition]:
        return typing.cast(typing.Optional[StorageBucketLifecycleRuleCondition], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketLifecycleRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketLifecycleRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketLifecycleRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e61cfe89aef1fa0500c07df10dd475975cbb2186f3cf5ee3da341a8c5081920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketLogging",
    jsii_struct_bases=[],
    name_mapping={"log_bucket": "logBucket", "log_object_prefix": "logObjectPrefix"},
)
class StorageBucketLogging:
    def __init__(
        self,
        *,
        log_bucket: builtins.str,
        log_object_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_bucket: The bucket that will receive log objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#log_bucket StorageBucket#log_bucket}
        :param log_object_prefix: The object prefix for log objects. If it's not provided, by default Google Cloud Storage sets this to this bucket's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#log_object_prefix StorageBucket#log_object_prefix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba22b184ac470c7b3dc9902518dfd4ae98dcffaa5e776c4a86379e09db20778)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#log_bucket StorageBucket#log_bucket}
        '''
        result = self._values.get("log_bucket")
        assert result is not None, "Required property 'log_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_object_prefix(self) -> typing.Optional[builtins.str]:
        '''The object prefix for log objects.

        If it's not provided, by default Google Cloud Storage sets this to this bucket's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#log_object_prefix StorageBucket#log_object_prefix}
        '''
        result = self._values.get("log_object_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketLogging(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketLoggingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketLoggingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3302752c92c649d70b11e46b52e9fd76f31489d4f324100a775bb46c6ba592b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5c14154f0d9b2b5d71131a935b0511c611c8fb82956025c20fc0afbb27758a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logObjectPrefix")
    def log_object_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logObjectPrefix"))

    @log_object_prefix.setter
    def log_object_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7cf2c850a3cf463b16380fb33b470a90164a316d6f4a4ebc2303fe94424a2ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logObjectPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBucketLogging]:
        return typing.cast(typing.Optional[StorageBucketLogging], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StorageBucketLogging]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752105bd7b2536dbfdd2a9f0a3e5ef4cd86523d386c6614b7fb76815d6616ffc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={"retention_period": "retentionPeriod", "is_locked": "isLocked"},
)
class StorageBucketRetentionPolicy:
    def __init__(
        self,
        *,
        retention_period: jsii.Number,
        is_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param retention_period: The period of time, in seconds, that objects in the bucket must be retained and cannot be deleted, overwritten, or archived. The value must be less than 3,155,760,000 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#retention_period StorageBucket#retention_period}
        :param is_locked: If set to true, the bucket will be locked and permanently restrict edits to the bucket's retention policy. Caution: Locking a bucket is an irreversible action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#is_locked StorageBucket#is_locked}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7c96689e4895a3a517516714152ca926700718825c72f351b80de2314d60951)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#retention_period StorageBucket#retention_period}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#is_locked StorageBucket#is_locked}
        '''
        result = self._values.get("is_locked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa519222614c64dfbfb38af235d2722d084ee12ceb43c8eb1db69aa734bb7ce1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__faaef7531b735fd4247102c637a51c4b418dee596714013be662d22e5ddf75c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isLocked", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPeriod")
    def retention_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriod"))

    @retention_period.setter
    def retention_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5b0db2028fd2b614baa4060de85704486a24af1959563e362986335551a95d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBucketRetentionPolicy]:
        return typing.cast(typing.Optional[StorageBucketRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageBucketRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0abd9e56cd9d04321c5b5993b857d3d427e01000c6c0e85d0598f7d4bbfe033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketSoftDeletePolicy",
    jsii_struct_bases=[],
    name_mapping={"retention_duration_seconds": "retentionDurationSeconds"},
)
class StorageBucketSoftDeletePolicy:
    def __init__(
        self,
        *,
        retention_duration_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param retention_duration_seconds: The duration in seconds that soft-deleted objects in the bucket will be retained and cannot be permanently deleted. Default value is 604800. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#retention_duration_seconds StorageBucket#retention_duration_seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45541c81af668fed40aa7c085b84b990a411287bec5c7bbc3570e60e1646bf17)
            check_type(argname="argument retention_duration_seconds", value=retention_duration_seconds, expected_type=type_hints["retention_duration_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if retention_duration_seconds is not None:
            self._values["retention_duration_seconds"] = retention_duration_seconds

    @builtins.property
    def retention_duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''The duration in seconds that soft-deleted objects in the bucket will be retained and cannot be permanently deleted.

        Default value is 604800.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#retention_duration_seconds StorageBucket#retention_duration_seconds}
        '''
        result = self._values.get("retention_duration_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketSoftDeletePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketSoftDeletePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketSoftDeletePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c50aabd9ec4d95b63746cf99db6539e0b305982b648281115c33063450f73a7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fabc3e3dcb5f60d2ffea80893ecf0491fafa356f41ce2a44a79eeb614397cd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDurationSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBucketSoftDeletePolicy]:
        return typing.cast(typing.Optional[StorageBucketSoftDeletePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageBucketSoftDeletePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__642b07bf2abd21b15164edf27dcea523eb4f3bd8b58e1006cbae7bd986a98b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "read": "read", "update": "update"},
)
class StorageBucketTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#create StorageBucket#create}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#read StorageBucket#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#update StorageBucket#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002247ec5b1236f3d4fd5f05c35979d694a5e06603405d2b95832ef6235470ec)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#create StorageBucket#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#read StorageBucket#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#update StorageBucket#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4277a4e9abf908d1e8677cfe41e1854be02a07f2f4670fb246fd87a9b90de94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2929db6de5819088af2c53b66d8c857c83581c82966b54e8d9a0977b4070102)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61ee65acfc7d65e6ecad3f500b5078802491923715b1614d2351261301899d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea2458cb99a2dd7e01cc92c69d2a16b591ae0b288d733cdb532ba00974022c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa685f2d636b7b777b6c75fa30f5f728b4a627a04052bb23494d7701210dcf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketVersioning",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class StorageBucketVersioning:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: While set to true, versioning is fully enabled for this bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#enabled StorageBucket#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea726803f2be5b028bf24561e638002d0c8a277304cce18c69fd244c7f2e97f0)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''While set to true, versioning is fully enabled for this bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#enabled StorageBucket#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketVersioning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketVersioningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketVersioningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1745ba7f1a276e74e30152b8b6b69503e3e83b0983b46809b42a50324cebf16e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__673cff8b21efa80a9035948a85ba8c40c9430881c98411c002715251e1b0dc63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBucketVersioning]:
        return typing.cast(typing.Optional[StorageBucketVersioning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StorageBucketVersioning]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978b2535c34d03580b9feda253982be64fb1e0b17840fad7dc4d8fb42af6b962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketWebsite",
    jsii_struct_bases=[],
    name_mapping={
        "main_page_suffix": "mainPageSuffix",
        "not_found_page": "notFoundPage",
    },
)
class StorageBucketWebsite:
    def __init__(
        self,
        *,
        main_page_suffix: typing.Optional[builtins.str] = None,
        not_found_page: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param main_page_suffix: Behaves as the bucket's directory index where missing objects are treated as potential directories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#main_page_suffix StorageBucket#main_page_suffix}
        :param not_found_page: The custom object to return when a requested resource is not found. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#not_found_page StorageBucket#not_found_page}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e36cc2465be0a4a81f17a8a38e13620c01c5df70a7a3b23cb8557a7d3ce5c784)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#main_page_suffix StorageBucket#main_page_suffix}
        '''
        result = self._values.get("main_page_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def not_found_page(self) -> typing.Optional[builtins.str]:
        '''The custom object to return when a requested resource is not found.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/storage_bucket#not_found_page StorageBucket#not_found_page}
        '''
        result = self._values.get("not_found_page")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageBucketWebsite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageBucketWebsiteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.storageBucket.StorageBucketWebsiteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2294e1e3003099ef32d7a291b38cff3f77d7996666b9c971414e8715cff8230)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0f1438d37c3a2f60d763fd7c8dd5b99cdae2b6fb7d27b539f80d2afa2e57d36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainPageSuffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notFoundPage")
    def not_found_page(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notFoundPage"))

    @not_found_page.setter
    def not_found_page(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821defc875191fce65b3f2af1d902bda3b92a87f58c1c55e1ac480ad8d25f1db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notFoundPage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageBucketWebsite]:
        return typing.cast(typing.Optional[StorageBucketWebsite], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StorageBucketWebsite]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794b9627c8856f5315e28a2a282c32a6610a6b8d0d5a5764d6077a0af15905b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StorageBucket",
    "StorageBucketAutoclass",
    "StorageBucketAutoclassOutputReference",
    "StorageBucketConfig",
    "StorageBucketCors",
    "StorageBucketCorsList",
    "StorageBucketCorsOutputReference",
    "StorageBucketCustomPlacementConfig",
    "StorageBucketCustomPlacementConfigOutputReference",
    "StorageBucketEncryption",
    "StorageBucketEncryptionOutputReference",
    "StorageBucketHierarchicalNamespace",
    "StorageBucketHierarchicalNamespaceOutputReference",
    "StorageBucketIpFilter",
    "StorageBucketIpFilterOutputReference",
    "StorageBucketIpFilterPublicNetworkSource",
    "StorageBucketIpFilterPublicNetworkSourceOutputReference",
    "StorageBucketIpFilterVpcNetworkSources",
    "StorageBucketIpFilterVpcNetworkSourcesList",
    "StorageBucketIpFilterVpcNetworkSourcesOutputReference",
    "StorageBucketLifecycleRule",
    "StorageBucketLifecycleRuleAction",
    "StorageBucketLifecycleRuleActionOutputReference",
    "StorageBucketLifecycleRuleCondition",
    "StorageBucketLifecycleRuleConditionOutputReference",
    "StorageBucketLifecycleRuleList",
    "StorageBucketLifecycleRuleOutputReference",
    "StorageBucketLogging",
    "StorageBucketLoggingOutputReference",
    "StorageBucketRetentionPolicy",
    "StorageBucketRetentionPolicyOutputReference",
    "StorageBucketSoftDeletePolicy",
    "StorageBucketSoftDeletePolicyOutputReference",
    "StorageBucketTimeouts",
    "StorageBucketTimeoutsOutputReference",
    "StorageBucketVersioning",
    "StorageBucketVersioningOutputReference",
    "StorageBucketWebsite",
    "StorageBucketWebsiteOutputReference",
]

publication.publish()

def _typecheckingstub__e744e8e397ebe7477262305eaa79414a8daecc81c0364a30bc93b0eeb7a4c659(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    autoclass: typing.Optional[typing.Union[StorageBucketAutoclass, typing.Dict[builtins.str, typing.Any]]] = None,
    cors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageBucketCors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_placement_config: typing.Optional[typing.Union[StorageBucketCustomPlacementConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_event_based_hold: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_object_retention: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption: typing.Optional[typing.Union[StorageBucketEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hierarchical_namespace: typing.Optional[typing.Union[StorageBucketHierarchicalNamespace, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_filter: typing.Optional[typing.Union[StorageBucketIpFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageBucketLifecycleRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    logging: typing.Optional[typing.Union[StorageBucketLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    public_access_prevention: typing.Optional[builtins.str] = None,
    requester_pays: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retention_policy: typing.Optional[typing.Union[StorageBucketRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    rpo: typing.Optional[builtins.str] = None,
    soft_delete_policy: typing.Optional[typing.Union[StorageBucketSoftDeletePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_class: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StorageBucketTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    uniform_bucket_level_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    versioning: typing.Optional[typing.Union[StorageBucketVersioning, typing.Dict[builtins.str, typing.Any]]] = None,
    website: typing.Optional[typing.Union[StorageBucketWebsite, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__80def101596c1c23b9348b9c0ec04c4df1a1ca684d1d2e9a9c8f9cb4e155c86a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d33be404b12e6bc299a9294405031bcde96d41876f6ef597a16bdd1c9084fb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageBucketCors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da96ca771ca4518f7bd37937e25d1001a9749f636947aeed73553c8170141a8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageBucketLifecycleRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c43eae756ecff4cd6f7b91f4ec11ed04440fcb71b243e49ce039c92ff6a9918(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e468f0387b1f9d2ffc8a55eebd5537c94e8b181f1cb1f446352f37e5baf4a0d8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb61d63720b396050733ba0d6474dfdb4c573f93d7ddfb5b884d5b9b15b5b742(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd1893c8c094bb11bc262d072489042671436b8c3fe6cc3a481beed8205ec85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a89d7701039dfac2be115c33e5e95fa1010b55cffa2edaf96117b847110e334(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91af7bcba55239c092d85914170cf06329955e61e9cb714f588fdcb4579d42b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b7353882c4f18e87609a1616df9e1f8d6861a51e07df819c80ea64fe976d367(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4037405b9499b1438ec04e86ae0cdd4a0f8036b3f77ab7ad3254af55d3f4640(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9db37c586455b1a77c043261511ab2c1467b9e14de30f8129304c312767aeaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a6d4447b1938cbba00fc73ebb836c6ec0a363a66ec9e642f96477929fc59f8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491beb0b40b7ffb57becd92dcb90591e292ea12e953393d6d13d516bc01845de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4ddcace566f24841caa5c561560251f9eaf34e7b5fc53ec165c1023d4be028(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e5e1e2b0f322395700141c6e81f5aad973f54de7b1b06f57b19c60c0ab00941(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8cff21a910b9b61ba752a0012d00077dae243fa135bfe26c4efbbfce20a1766(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    terminal_storage_class: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a0996c9b00ca79d1b6ca5fe535ad5d859258806c52208f814a30efa4568172(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b771d700f0a859e7980db8ea0ad41978ab16a5b9c08e23a2de523faaffac29(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907826594ff7810e451d09868e94345e2c74a71d4d19b3481126675d1c92cd51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951b9f16ba08ae05418f2f1f9e25ff7a8a67e5f9c7682f645a0a9d485ec2e84e(
    value: typing.Optional[StorageBucketAutoclass],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d74d186ee8573d20d9bfd535070f237fc48472bb2a3bfe49962236f91ed4a86(
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
    autoclass: typing.Optional[typing.Union[StorageBucketAutoclass, typing.Dict[builtins.str, typing.Any]]] = None,
    cors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageBucketCors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_placement_config: typing.Optional[typing.Union[StorageBucketCustomPlacementConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_event_based_hold: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_object_retention: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption: typing.Optional[typing.Union[StorageBucketEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hierarchical_namespace: typing.Optional[typing.Union[StorageBucketHierarchicalNamespace, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_filter: typing.Optional[typing.Union[StorageBucketIpFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lifecycle_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageBucketLifecycleRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    logging: typing.Optional[typing.Union[StorageBucketLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    public_access_prevention: typing.Optional[builtins.str] = None,
    requester_pays: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retention_policy: typing.Optional[typing.Union[StorageBucketRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    rpo: typing.Optional[builtins.str] = None,
    soft_delete_policy: typing.Optional[typing.Union[StorageBucketSoftDeletePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_class: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StorageBucketTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    uniform_bucket_level_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    versioning: typing.Optional[typing.Union[StorageBucketVersioning, typing.Dict[builtins.str, typing.Any]]] = None,
    website: typing.Optional[typing.Union[StorageBucketWebsite, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef412622584f98b084b338d3d4617546429e4bcc4a1890188e397260f9aba4a(
    *,
    max_age_seconds: typing.Optional[jsii.Number] = None,
    method: typing.Optional[typing.Sequence[builtins.str]] = None,
    origin: typing.Optional[typing.Sequence[builtins.str]] = None,
    response_header: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cfcc2af4509c613f0b10e3f70aadcc5f3a0ebab463d62e0a0afb8e836a6f4bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87342c5fc1eceafe645dca3d5f9649f12d0ce39fdc1560bafaf40351477e997c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff1d56728aed59557b642e045353d68e3ac8e645fd6de91e9e3aaba1dcd60ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32a7a46ae22349f98086db40b2983b977e28b17524513df307f2ab9ea9d8541a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dfa836c103a07baeef6370f36034b124c2133af8a1bd235ccf16c40d044f7e7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e642000d4f6bc88b80ff0fcfe61614a26781fae006c7ecf751010218b3a1b1e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageBucketCors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e553d4ca7afc37244257225bdb272bdc0ca0be50eaa20607f38fa4418bf0dd2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d61147263d9216a83b53e00a4dfe23d4504b2d15581190498765bcd302efc2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e522e6664a079012e73adf2db5613f04b507880d59b39759b5e4ecb866b7957(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144757fefde1a67186bb8cc53b3d28ad2fe508315ca2650061df4aab039eac64(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0a04672b1337fb5032a777e7133486ce1bb385206be806e262101be750b6af(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a600eaa092abd30a72b58b4f40707250019b798aed12c136d7d7159c2959879(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketCors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be966fd842cb3b190260f703dc8f02f24e359b7144512e40d5c3088035f70986(
    *,
    data_locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ad3e3a6fc39e25d0056c473a974a0afd47b0386d0509a051938a7ca65038c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fdc904692d400a50c3c578a54d5dfc009a743132db1077e9070763a45ab5ece(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0382ea66a6b6cda39c04ed4b095e7cdc2dad4c41493ff7af5d9fbe1875818d15(
    value: typing.Optional[StorageBucketCustomPlacementConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233e32da1f81399aa3046393c53d55c23ba834bd7e142ddaae4c88fcf80886d9(
    *,
    default_kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340fbc3369a5aafd0152aac7fbd7d02e51f180e0e9ac85883ad535e1dea8ff3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f291091cc3ace1ba31cca014095424910b8b7b26bacc254f1cd651c6a0f500d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98d7b1c0bdc44a0990d33673e6a105f06939fc121f9b133721afe806a8da1ab(
    value: typing.Optional[StorageBucketEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834d242bb36366b1c04219c3bdc78f160e0d2100216e4daca2cb83178c4f28e4(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a8e6eb37407b8d2a9a3afb876a45d0843fb990c976d7c473649c597077ebfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72aa09511f5736841d9055cd338dc6b6762d3c1894e3610af17696efe849990(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3789277a693f3407b19afe162ba91723e0ddb5fdd01996c025b83f89eed6cf(
    value: typing.Optional[StorageBucketHierarchicalNamespace],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d460705e4a65c23dc8c2700f96b8f966196387db9ccfaa23bb1ca526355227(
    *,
    mode: builtins.str,
    allow_all_service_agent_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_cross_org_vpcs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_network_source: typing.Optional[typing.Union[StorageBucketIpFilterPublicNetworkSource, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_network_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageBucketIpFilterVpcNetworkSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08449c4c0934b6fdc895db577a9d99ed00ee6827254e7a726ddb35c9babbbc1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a327456067142a12ab41851fd18290bb589aec2dcc41643822e4cc84d9124c3a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageBucketIpFilterVpcNetworkSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b6b5b7c68cf5c312ac1816c7e79cbdef70007c25e00d2ca1569bf4acd40986e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dfdc2e59c0c0a3ac5d0014c957869d1ae820237fcf972123a90e8eb177efe7f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530e56480d5fa9ef176b6f6a4f67f4bd7b3282ee984973412dd7425b6090f22c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5dd3d2a000301a5325dd57784e7eaf1af697ba09cb88c680c44a8aa5c7207de(
    value: typing.Optional[StorageBucketIpFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177a019124eed5ee07ad95775b50cf2f7c68a20c219e00f61cb5bb223f67b683(
    *,
    allowed_ip_cidr_ranges: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cacd93b8395869e6eeaeed91f814b4b24754a25210c8129e826f784ad15b988(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513070bc23da80eff4a4e3af151fb9688bfd3b85aaea9ed94f3ec902abc7d84f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68958f8db9ff009b64bbdec93229804a1d5c6709f8468eff485a0eb0c731b91f(
    value: typing.Optional[StorageBucketIpFilterPublicNetworkSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf796e130e66a1873a80b2dec977096bd0536550632f744cd324991bfd49732c(
    *,
    allowed_ip_cidr_ranges: typing.Sequence[builtins.str],
    network: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54adb5a6b6fe6e5fb87b81c0eea75dba9afb3b9bf7117abece9fc4a766723c3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b99843ae8fc252bf83329cd8eea873083afff226fefbd8902e756e86eeaeb8a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fcba357f3fd98ce7a87ff977eb73da5838e6e60b54fe2218f46ae0dd2d3e8e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c43dbc33a3b31bfe88bec371944217fbe182fd0a80a44cd7182cd719a639ff8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__831499a9c03ee051b40151ec4e24674fdd944cb1f18a00a9ef233b7e9477ae00(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7812cc02ac4f14682abe4f17ea3fa8ffcbfe235133038787c6625b744f1f42(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageBucketIpFilterVpcNetworkSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb0563c7860bdbf7976687809c06bd5e140a2162f964a9d75b3cd885259c4ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cffb0861b7dc0b0a2bca8ececd0f1f8b58783c6ee6d01d49c18d5f0922847ee8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2624b6c9bdf526c1493778734969b25b6a9915e7a47f2ac35df7e1f58cedf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a238df146cbcec9d3e14555b8ec1e430793cd98ef21a9d477a76e6c4a4a34b40(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketIpFilterVpcNetworkSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58a152ae184b9c2f7237dcc670223a18cc3f24e301b4fb3a4664c4c1a00365a(
    *,
    action: typing.Union[StorageBucketLifecycleRuleAction, typing.Dict[builtins.str, typing.Any]],
    condition: typing.Union[StorageBucketLifecycleRuleCondition, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d9ff233c9198bbe2da4e903fe40cf1bf2aedfb779151f8b920f57a701d6a0dd(
    *,
    type: builtins.str,
    storage_class: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311817abe6861caf53cb3e32d8c7b0152aed06fa168d6aea74d60946b749a1aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e3164cc155286ccc974c1a71dcf811c76f00cdc880e94494c7663ad2f3a267(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfef90eeb6ce020a96dc2f0e2413d379d62df49c658849f9f680595e362b8e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7573ff92eefa7bcc68024c6038b20bb839ccd158b3c892871c996cfedf49cfd(
    value: typing.Optional[StorageBucketLifecycleRuleAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8aac0cdf7077b6114d49ee6654a4780e1eddc86fc3a941ab4cd9acaae68ba4b(
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

def _typecheckingstub__433dcac421ee8e506852b692e5e2e8518f8b59710ee1b615e5915c3693c90f67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4f4538fcd5caf334758699f364936b69b0718a2814ed82a0d997de6e7b6b0e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09458f9213df6b0229026994cd1bf98da0e7fa3a7f21458fbcf88f7fc0b742dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aae13f8132abf7ff829d8f7f58fcf3a9f6aae86eb329e361ed73b19d003f05e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946735d8eeb03e951d3da5911efe846cfd9e35cf45ea881c3d8b9fcdc095fca8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff770efd8bd5a9d3d470c48d8a135842abc97eaa37ff0602a6cce6edab2281c1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec996d21b3decc6970a8c7b526726122c3c7e65b0ff79c77d1328eb9de5c2dcf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa245f7ab118cc55d517bf2e6cafb0ea179140da3a5f5a6138d6efd75dd8b5a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7cef68a55671fced4f273265a81e741c86e32931f8335f710f109f62f71f402(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33414a496a8714c1985c8193612e3616a030265b21b74a4213909bbe3813b8d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101480b6bafc9e0d78fec9df6a083de7172cfdd584dd3b0eb2e2382af1163bf2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86351a822e237a41c07ddbc2026cbff51f8fa2a90b4587d2a8ca3dd0cdfe4ac8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc82e1e252781474046be8c851efc6f69bf0481bdf8ab512cbad7633b14931e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe8291f3ab90ed5ba81d64b4147556a8c50837815fdbd060568aa99eebe313a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297151f9e680026d033e09dc565d655dd7ced014f0fd0f82c04e359597ee9df7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956645a973c9f0a2bffa09a4bd836443f13726b42b4f0a3aca5e5245da2d7d6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0225d3a07e1cc7fa6c2b92d84bef5d792c0e14f70d0d3118cd25e3b2356d7e8c(
    value: typing.Optional[StorageBucketLifecycleRuleCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca3a82a285a501ba71ce714a649e353bec15a214806168c70930075d9da71ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049b0a552d3f0a3efc1581a9ba89ad62335ffbdb5ef06a18a720621f2b2c6f46(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a735e43291c656843d100e80270a3141ed7cb08802ff45180947adcfde0af5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7989d0a997476734a09ff95644a9ecbc9d43b1df22d91bee5c43e9b7e96b591d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf43a2da1ff5823dbab67dcce6453b26fb42e3d93f29efcf75c3d066b53208e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4403f4133b4cddfbc3dd149dd930a3478130a3a984672a74c7f17240ada7b333(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageBucketLifecycleRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3088596f13a0abc5f8c56446774236ffc218168da2c83899637d28af1501988f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e61cfe89aef1fa0500c07df10dd475975cbb2186f3cf5ee3da341a8c5081920(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketLifecycleRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba22b184ac470c7b3dc9902518dfd4ae98dcffaa5e776c4a86379e09db20778(
    *,
    log_bucket: builtins.str,
    log_object_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3302752c92c649d70b11e46b52e9fd76f31489d4f324100a775bb46c6ba592b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c14154f0d9b2b5d71131a935b0511c611c8fb82956025c20fc0afbb27758a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7cf2c850a3cf463b16380fb33b470a90164a316d6f4a4ebc2303fe94424a2ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752105bd7b2536dbfdd2a9f0a3e5ef4cd86523d386c6614b7fb76815d6616ffc(
    value: typing.Optional[StorageBucketLogging],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c96689e4895a3a517516714152ca926700718825c72f351b80de2314d60951(
    *,
    retention_period: jsii.Number,
    is_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa519222614c64dfbfb38af235d2722d084ee12ceb43c8eb1db69aa734bb7ce1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faaef7531b735fd4247102c637a51c4b418dee596714013be662d22e5ddf75c1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b0db2028fd2b614baa4060de85704486a24af1959563e362986335551a95d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0abd9e56cd9d04321c5b5993b857d3d427e01000c6c0e85d0598f7d4bbfe033(
    value: typing.Optional[StorageBucketRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45541c81af668fed40aa7c085b84b990a411287bec5c7bbc3570e60e1646bf17(
    *,
    retention_duration_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50aabd9ec4d95b63746cf99db6539e0b305982b648281115c33063450f73a7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fabc3e3dcb5f60d2ffea80893ecf0491fafa356f41ce2a44a79eeb614397cd9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642b07bf2abd21b15164edf27dcea523eb4f3bd8b58e1006cbae7bd986a98b39(
    value: typing.Optional[StorageBucketSoftDeletePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002247ec5b1236f3d4fd5f05c35979d694a5e06603405d2b95832ef6235470ec(
    *,
    create: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4277a4e9abf908d1e8677cfe41e1854be02a07f2f4670fb246fd87a9b90de94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2929db6de5819088af2c53b66d8c857c83581c82966b54e8d9a0977b4070102(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61ee65acfc7d65e6ecad3f500b5078802491923715b1614d2351261301899d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea2458cb99a2dd7e01cc92c69d2a16b591ae0b288d733cdb532ba00974022c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa685f2d636b7b777b6c75fa30f5f728b4a627a04052bb23494d7701210dcf8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageBucketTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea726803f2be5b028bf24561e638002d0c8a277304cce18c69fd244c7f2e97f0(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1745ba7f1a276e74e30152b8b6b69503e3e83b0983b46809b42a50324cebf16e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673cff8b21efa80a9035948a85ba8c40c9430881c98411c002715251e1b0dc63(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978b2535c34d03580b9feda253982be64fb1e0b17840fad7dc4d8fb42af6b962(
    value: typing.Optional[StorageBucketVersioning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36cc2465be0a4a81f17a8a38e13620c01c5df70a7a3b23cb8557a7d3ce5c784(
    *,
    main_page_suffix: typing.Optional[builtins.str] = None,
    not_found_page: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2294e1e3003099ef32d7a291b38cff3f77d7996666b9c971414e8715cff8230(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f1438d37c3a2f60d763fd7c8dd5b99cdae2b6fb7d27b539f80d2afa2e57d36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821defc875191fce65b3f2af1d902bda3b92a87f58c1c55e1ac480ad8d25f1db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794b9627c8856f5315e28a2a282c32a6610a6b8d0d5a5764d6077a0af15905b1(
    value: typing.Optional[StorageBucketWebsite],
) -> None:
    """Type checking stubs"""
    pass
